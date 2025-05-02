from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import User, Doctor, Speciality, Location, Appointment
from django.utils import timezone
import datetime
from django.contrib.auth.hashers import make_password
import os
from django.conf import settings

def search_doctors(request):
    """View to search for doctors by speciality and location"""
    specialities = Speciality.objects.all()
    locations = Location.objects.all()
    
    # Default: show all doctors
    doctors = Doctor.objects.all()
    
    # Search by speciality or doctor name
    if 'search_doctor' in request.GET and request.GET['search_doctor']:
        search_query = request.GET['search_doctor']
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) | 
            Q(user__last_name__icontains=search_query) |
            Q(speciality__name__icontains=search_query)
        )
    
    # Search by location
    if 'search_location' in request.GET and request.GET['search_location']:
        location_query = request.GET['search_location']
        doctors = doctors.filter(
            Q(location__name__icontains=location_query) |
            Q(location__city__icontains=location_query) |
            Q(location__state__icontains=location_query)
        )
    
    context = {
        'doctors': doctors,
        'specialities': specialities,
        'locations': locations
    }
    
    return render(request, 'doctors_list.html', context)

def doctor_detail(request, doctor_id):
    """View to display doctor details and appointment booking form"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Get available times for next 7 days
    available_dates = []
    today = timezone.now().date()
    
    for i in range(7):
        date = today + datetime.timedelta(days=i)
        day_name = date.strftime('%A')
        
        # Check if doctor is available on this day
        if day_name in doctor.available_days:
            available_dates.append(date)
    
    context = {
        'doctor': doctor,
        'available_dates': available_dates
    }
    
    return render(request, 'doctor_detail.html', context)

@login_required
def book_appointment(request, doctor_id):
    """View to book an appointment with a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        date_str = request.POST.get('appointment_date')
        time_str = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms', '')
        
        try:
            # Parse date and time
            appointment_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment_time = datetime.datetime.strptime(time_str, '%H:%M').time()
            
            # Check if appointment is in the past
            if appointment_date < timezone.now().date():
                messages.error(request, "You cannot book an appointment in the past.")
                return redirect('doctor_detail', doctor_id=doctor.id)
            
            # Check if the appointment time is within doctor's available hours
            if (appointment_time < doctor.available_time_start or 
                appointment_time > doctor.available_time_end):
                messages.error(request, "The selected time is outside doctor's available hours.")
                return redirect('doctor_detail', doctor_id=doctor.id)
            
            # Check if the doctor already has an appointment at this time
            if Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            ).exists():
                messages.error(request, "This time slot is already booked. Please select another time.")
                return redirect('doctor_detail', doctor_id=doctor.id)
            
            # Create the appointment
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                symptoms=symptoms,
                status='pending'
            )
            
            messages.success(request, "Appointment requested successfully!")
            return redirect('my_appointments')
            
        except Exception as e:
            messages.error(request, f"Error booking appointment: {str(e)}")
            return redirect('doctor_detail', doctor_id=doctor.id)
    
    # If GET request, redirect to doctor detail page
    return redirect('doctor_detail', doctor_id=doctor.id)

@login_required
def my_appointments(request):
    """View to display user's appointments"""
    if request.user.is_doctor:
        # Doctor sees appointments where they are the doctor
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    else:
        # Patient sees appointments where they are the patient
        appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')
    
    context = {
        'appointments': appointments
    }
    
    return render(request, 'my_appointments.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    """View to cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is authorized to cancel this appointment
    if request.user == appointment.patient or request.user == appointment.doctor.user:
        if appointment.status not in ['completed', 'cancelled']:
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, "Appointment cancelled successfully.")
        else:
            messages.error(request, "Cannot cancel a completed or already cancelled appointment.")
    else:
        messages.error(request, "You are not authorized to cancel this appointment.")
    
    return redirect('my_appointments')

@login_required
def update_appointment(request, appointment_id):
    """View to update appointment status (for doctors)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is the doctor for this appointment
    try:
        doctor = Doctor.objects.get(user=request.user)
        if appointment.doctor != doctor:
            messages.error(request, "You are not authorized to update this appointment.")
            return redirect('my_appointments')
    except Doctor.DoesNotExist:
        messages.error(request, "Only doctors can update appointment status.")
        return redirect('my_appointments')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['confirmed', 'completed', 'cancelled']:
            appointment.status = status
            appointment.save()
            messages.success(request, f"Appointment status updated to {status}.")
        else:
            messages.error(request, "Invalid status provided.")
    
    return redirect('my_appointments')

# Hospital Admin Views
@login_required(login_url='/admin-login/')
def admin_dashboard(request):
    """View for hospital admin dashboard"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    # Get counts for dashboard
    total_doctors = Doctor.objects.count()
    total_patients = User.objects.filter(is_patient=True).count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    
    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required(login_url='/admin-login/')
def admin_manage_appointments(request):
    """View for hospital admin to manage all appointments"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    appointments = Appointment.objects.all().order_by('-appointment_date')
    
    context = {
        'appointments': appointments
    }
    
    return render(request, 'admin_appointments.html', context)

@login_required(login_url='/admin-login/')
def admin_update_appointment(request, appointment_id):
    """View for hospital admin to update appointment status"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'confirmed', 'completed', 'cancelled']:
            appointment.status = status
            appointment.save()
            messages.success(request, f"Appointment status updated to {status}.")
        else:
            messages.error(request, "Invalid status provided.")
    
    return redirect('admin_manage_appointments')

@login_required(login_url='/admin-login/')
def admin_doctors_list(request):
    """View for hospital admin to see all doctors"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    doctors = Doctor.objects.all()
    
    context = {
        'doctors': doctors
    }
    
    return render(request, 'admin_doctors.html', context)

@login_required(login_url='/admin-login/')
def admin_add_doctor(request):
    """View for hospital admin to add a new doctor"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    specialties = Speciality.objects.all()
    locations = Location.objects.all()
    
    if request.method == 'POST':
        try:
            # Get form data
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile = request.POST.get('mobile')
            city = request.POST.get('city')
            specialty_id = request.POST.get('specialty')
            experience = request.POST.get('experience')
            fee = request.POST.get('fee')
            location_id = request.POST.get('location')
            available_days = request.POST.get('available_days')
            available_time_start = request.POST.get('available_time_start')
            available_time_end = request.POST.get('available_time_end')
            
            # Handle profile image upload
            profile_image = request.FILES.get('profile_image')
            image_path = "/static/images/doctor-avatar.png"  # Default image path
            
            if profile_image:
                # Create the profile photos directory if it doesn't exist
                profile_dir = os.path.join(settings.STATIC_ROOT, 'images', 'profilephotos')
                os.makedirs(profile_dir, exist_ok=True)
                
                # Generate a unique filename
                filename = f"{first_name}_{last_name}_{int(timezone.now().timestamp())}.jpg"
                file_path = os.path.join(profile_dir, filename)
                
                # Save the image
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_image.chunks():
                        destination.write(chunk)
                
                # Update the image path
                image_path = f"/static/images/profilephotos/{filename}"
            
            # Create user
            doctor_user = User.objects.create(
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                city=city,
                is_patient=False,
                is_doctor=True
            )
            
            # Create doctor profile
            doctor_profile = Doctor.objects.create(
                user=doctor_user,
                speciality_id=specialty_id,
                experience=experience,
                fee=fee,
                location_id=location_id,
                available_days=available_days,
                available_time_start=available_time_start,
                available_time_end=available_time_end,
                profile_image=image_path
            )
            
            messages.success(request, f"Doctor {first_name} {last_name} added successfully!")
            return redirect('admin_doctors_list')
            
        except Exception as e:
            messages.error(request, f"Error adding doctor: {str(e)}")
    
    context = {
        'specialties': specialties,
        'locations': locations
    }
    
    return render(request, 'admin_add_doctor.html', context)

@login_required(login_url='/admin-login/')
def admin_edit_doctor(request, doctor_id):
    """View for hospital admin to edit a doctor"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    specialties = Speciality.objects.all()
    locations = Location.objects.all()
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        specialty_id = request.POST.get('specialty')
        experience = request.POST.get('experience')
        fee = request.POST.get('fee')
        location_id = request.POST.get('location')
        available_days = request.POST.get('available_days')
        available_time_start = request.POST.get('available_time_start')
        available_time_end = request.POST.get('available_time_end')
        
        try:
            # Update user
            doctor.user.first_name = first_name
            doctor.user.last_name = last_name
            doctor.user.mobile = mobile
            doctor.user.city = city
            doctor.user.save()
            
            # Update doctor profile
            doctor.speciality_id = specialty_id
            doctor.experience = experience
            doctor.fee = fee
            doctor.location_id = location_id
            doctor.available_days = available_days
            doctor.available_time_start = available_time_start
            doctor.available_time_end = available_time_end
            doctor.save()
            
            messages.success(request, f"Doctor {first_name} {last_name} updated successfully!")
            return redirect('admin_doctors_list')
            
        except Exception as e:
            messages.error(request, f"Error updating doctor: {str(e)}")
    
    context = {
        'doctor': doctor,
        'specialties': specialties,
        'locations': locations
    }
    
    return render(request, 'admin_edit_doctor.html', context)

@login_required(login_url='/admin-login/')
def admin_delete_doctor(request, doctor_id):
    """View for hospital admin to delete a doctor"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        try:
            user = doctor.user
            doctor.delete()
            user.delete()
            messages.success(request, "Doctor deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting doctor: {str(e)}")
    
    return redirect('admin_doctors_list')

@login_required(login_url='/admin-login/')
def admin_specialities(request):
    """View for hospital admin to manage specialities"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    specialities = Speciality.objects.all()
    
    context = {
        'specialities': specialities
    }
    
    return render(request, 'admin_specialities.html', context)

@login_required(login_url='/admin-login/')
def admin_add_speciality(request):
    """View for hospital admin to add a new speciality"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.POST.get('image')
        
        try:
            Speciality.objects.create(
                name=name,
                description=description,
                image=image
            )
            messages.success(request, f"Speciality '{name}' added successfully!")
            return redirect('admin_specialities')
        except Exception as e:
            messages.error(request, f"Error adding speciality: {str(e)}")
    
    return render(request, 'admin_add_speciality.html')

@login_required(login_url='/admin-login/')
def admin_edit_speciality(request, speciality_id):
    """View for hospital admin to edit a speciality"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    try:
        speciality = Speciality.objects.get(id=speciality_id)
    except Speciality.DoesNotExist:
        messages.error(request, "Speciality not found.")
        return redirect('admin_specialities')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        try:
            speciality.name = name
            speciality.description = description
            speciality.save()
            messages.success(request, f"Speciality '{name}' updated successfully!")
            return redirect('admin_specialities')
        except Exception as e:
            messages.error(request, f"Error updating speciality: {str(e)}")
    
    return redirect('admin_specialities')

@login_required(login_url='/admin-login/')
def admin_delete_speciality(request, speciality_id):
    """View for hospital admin to delete a speciality"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    try:
        speciality = Speciality.objects.get(id=speciality_id)
        speciality_name = speciality.name
        
        # Check if speciality is associated with any doctors
        doctor_count = Doctor.objects.filter(speciality=speciality).count()
        if doctor_count > 0:
            messages.error(request, f"Cannot delete speciality '{speciality_name}' as it is associated with {doctor_count} doctor(s).")
            return redirect('admin_specialities')
        
        speciality.delete()
        messages.success(request, f"Speciality '{speciality_name}' deleted successfully!")
    except Speciality.DoesNotExist:
        messages.error(request, "Speciality not found.")
    except Exception as e:
        messages.error(request, f"Error deleting speciality: {str(e)}")
    
    return redirect('admin_specialities')

@login_required(login_url='/admin-login/')
def admin_appointment_detail(request, appointment_id):
    """View for hospital admin to see appointment details"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    context = {
        'appointment': appointment
    }
    
    return render(request, 'admin_appointment_detail.html', context)

@login_required(login_url='/admin-login/')
def admin_update_appointment_status(request, appointment_id):
    """View for hospital admin to update appointment status"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'confirmed', 'completed', 'cancelled']:
            appointment.status = status
            appointment.save()
            messages.success(request, f"Appointment status updated to {status}.")
        else:
            messages.error(request, "Invalid status provided.")
    
    return redirect('admin_appointment_detail', appointment_id=appointment_id)

@login_required(login_url='/admin-login/')
def admin_edit_appointment(request, appointment_id):
    """View for hospital admin to edit an appointment"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    
    if request.method == 'POST':
        # Get form data
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms')
        
        try:
            # Update appointment
            appointment.doctor_id = doctor_id
            appointment.appointment_date = appointment_date
            appointment.appointment_time = appointment_time
            appointment.symptoms = symptoms
            appointment.save()
            
            messages.success(request, "Appointment updated successfully!")
            return redirect('admin_appointment_detail', appointment_id=appointment_id)
            
        except Exception as e:
            messages.error(request, f"Error updating appointment: {str(e)}")
    
    context = {
        'appointment': appointment,
        'doctors': doctors
    }
    
    return render(request, 'admin_edit_appointment.html', context)

@login_required(login_url='/admin-login/')
def admin_delete_appointment(request, appointment_id):
    """View for hospital admin to permanently delete an appointment"""
    if not request.user.is_hospital_admin:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    try:
        # Permanently delete the appointment from the database
        appointment.delete()
        messages.success(request, "Appointment permanently deleted.")
    except Exception as e:
        messages.error(request, f"Error deleting appointment: {str(e)}")
    
    return redirect('admin_manage_appointments')
