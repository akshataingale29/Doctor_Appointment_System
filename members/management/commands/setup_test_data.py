from django.core.management.base import BaseCommand
from django.db import transaction
from members.models import User, Speciality, Location, Doctor
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import datetime

class Command(BaseCommand):
    help = 'Setup test data for the doctor appointment system'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up test data...'))
        
        # Create specialties
        specialties = [
            {
                'name': 'Cardiology',
                'description': 'Cardiology is a branch of medicine that deals with disorders of the heart and the cardiovascular system.',
                'image': '/static/images/Cardiology.png'
            },
            {
                'name': 'Dermatology',
                'description': 'Dermatology is the branch of medicine dealing with the skin. It is a specialty with both medical and surgical aspects.',
                'image': '/static/images/Darmatology.jpeg'
            },
            {
                'name': 'ENT',
                'description': 'Otorhinolaryngology is a surgical subspecialty within medicine that deals with the surgical and medical management of conditions of the head and neck.',
                'image': '/static/images/ENT.jpeg'
            },
            {
                'name': 'Gastroenterology',
                'description': 'Gastroenterology is the branch of medicine focused on the digestive system and its disorders.',
                'image': '/static/images/Gastroinstential.jpeg'
            },
            {
                'name': 'Dental Care',
                'description': 'Dentistry, also known as dental medicine and oral medicine, is the branch of medicine focused on the teeth, gums, and mouth.',
                'image': '/static/images/Dentalcare.png'
            },
        ]
        
        created_specialties = []
        for specialty_data in specialties:
            specialty, created = Speciality.objects.get_or_create(
                name=specialty_data['name'],
                defaults={
                    'description': specialty_data['description'],
                    'image': specialty_data['image']
                }
            )
            created_specialties.append(specialty)
            action = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f"{action}: Specialty '{specialty.name}'"))
        
        # Create locations
        locations = [
            {
                'name': 'City Hospital',
                'address': '123 Main Street',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400001'
            },
            {
                'name': 'Health Plus Clinic',
                'address': '456 Park Avenue',
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001'
            },
            {
                'name': 'MedCare Hospital',
                'address': '789 Lake Road',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001'
            },
            {
                'name': 'Wellness Center',
                'address': '321 Gandhi Road',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'pincode': '600001'
            },
        ]
        
        created_locations = []
        for location_data in locations:
            location, created = Location.objects.get_or_create(
                name=location_data['name'],
                defaults={
                    'address': location_data['address'],
                    'city': location_data['city'],
                    'state': location_data['state'],
                    'pincode': location_data['pincode']
                }
            )
            created_locations.append(location)
            action = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f"{action}: Location '{location.name}'"))
        
        # Create doctor users and profiles
        doctors_data = [
            {
                'email': 'dr.sharma@example.com',
                'password': 'doctor123',
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'mobile': '9876543210',
                'city': 'Mumbai',
                'specialty_index': 0,  # Cardiology
                'location_index': 0,  # City Hospital
                'experience': 15,
                'fee': 1500,
                'available_days': 'Monday,Wednesday,Friday',
                'available_time_start': datetime.time(9, 0),
                'available_time_end': datetime.time(17, 0)
            },
            {
                'email': 'dr.patel@example.com',
                'password': 'doctor123',
                'first_name': 'Nisha',
                'last_name': 'Patel',
                'mobile': '9876543211',
                'city': 'Delhi',
                'specialty_index': 1,  # Dermatology
                'location_index': 1,  # Health Plus Clinic
                'experience': 8,
                'fee': 1200,
                'available_days': 'Tuesday,Thursday,Saturday',
                'available_time_start': datetime.time(10, 0),
                'available_time_end': datetime.time(18, 0)
            },
            {
                'email': 'dr.gupta@example.com',
                'password': 'doctor123',
                'first_name': 'Anil',
                'last_name': 'Gupta',
                'mobile': '9876543212',
                'city': 'Bangalore',
                'specialty_index': 2,  # ENT
                'location_index': 2,  # MedCare Hospital
                'experience': 12,
                'fee': 1300,
                'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
                'available_time_start': datetime.time(8, 0),
                'available_time_end': datetime.time(16, 0)
            },
            {
                'email': 'dr.reddy@example.com',
                'password': 'doctor123',
                'first_name': 'Suman',
                'last_name': 'Reddy',
                'mobile': '9876543213',
                'city': 'Chennai',
                'specialty_index': 3,  # Gastroenterology
                'location_index': 3,  # Wellness Center
                'experience': 20,
                'fee': 2000,
                'available_days': 'Wednesday,Thursday,Friday,Saturday',
                'available_time_start': datetime.time(9, 30),
                'available_time_end': datetime.time(17, 30)
            },
            {
                'email': 'dr.singh@example.com',
                'password': 'doctor123',
                'first_name': 'Harpreet',
                'last_name': 'Singh',
                'mobile': '9876543214',
                'city': 'Mumbai',
                'specialty_index': 4,  # Dental Care
                'location_index': 0,  # City Hospital
                'experience': 10,
                'fee': 1000,
                'available_days': 'Monday,Tuesday,Saturday',
                'available_time_start': datetime.time(11, 0),
                'available_time_end': datetime.time(19, 0)
            },
        ]
        
        for doctor_data in doctors_data:
            doctor_user, created = User.objects.get_or_create(
                email=doctor_data['email'],
                defaults={
                    'password': make_password(doctor_data['password']),
                    'first_name': doctor_data['first_name'],
                    'last_name': doctor_data['last_name'],
                    'mobile': doctor_data['mobile'],
                    'city': doctor_data['city'],
                    'is_patient': False,
                    'is_doctor': True
                }
            )
            action = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f"{action}: Doctor user '{doctor_user.email}'"))
            
            if created or not hasattr(doctor_user, 'doctor_profile'):
                doctor_profile = Doctor.objects.create(
                    user=doctor_user,
                    speciality=created_specialties[doctor_data['specialty_index']],
                    experience=doctor_data['experience'],
                    fee=doctor_data['fee'],
                    location=created_locations[doctor_data['location_index']],
                    available_days=doctor_data['available_days'],
                    available_time_start=doctor_data['available_time_start'],
                    available_time_end=doctor_data['available_time_end']
                )
                self.stdout.write(self.style.SUCCESS(f"Created: Doctor profile for {doctor_user.first_name} {doctor_user.last_name}"))
        
        # Create a test patient account
        patient_user, created = User.objects.get_or_create(
            email='patient@example.com',
            defaults={
                'password': make_password(''),
                'first_name': 'Test',
                'last_name': 'Patient',
                'mobile': '9876543215',
                'city': 'Mumbai',
                'is_patient': True,
                'is_doctor': False
            }
        )
        action = 'Created' if created else 'Already exists'
        self.stdout.write(self.style.SUCCESS(f"{action}: Patient user '{patient_user.email}'"))
        
        # Create a hospital admin account
        admin_user, created = User.objects.get_or_create(
            email='admin@hospital.com',
            defaults={
                'password': make_password('admin123'),
                'first_name': 'Hospital',
                'last_name': 'Admin',
                'mobile': '9876543216',
                'city': 'Mumbai',
                'is_patient': False,
                'is_doctor': False,
                'is_hospital_admin': True
            }
        )
        action = 'Created' if created else 'Already exists'
        self.stdout.write(self.style.SUCCESS(f"{action}: Hospital Admin user '{admin_user.email}'"))
        
        self.stdout.write(self.style.SUCCESS('Test data setup complete!'))
        self.stdout.write(self.style.SUCCESS('Test patient login: patient@example.com / patient123'))
        self.stdout.write(self.style.SUCCESS('Test doctor login: dr.sharma@example.com / doctor123'))
        self.stdout.write(self.style.SUCCESS('Test admin login: admin@hospital.com / admin123')) 