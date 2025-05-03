from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
import uuid

class User(AbstractUser):

    username=None
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=14)
    city=models.CharField(max_length=100)
    
    # Add fields to identify user type
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_hospital_admin = models.BooleanField(default=False)

    objects=UserManager()
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)  # Path to image
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Specialities"

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    experience = models.PositiveIntegerField(default=0)  # Experience in years
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    available_days = models.CharField(max_length=100, default="Monday-Friday")  # e.g. "Monday,Wednesday,Friday"
    available_time_start = models.TimeField(default="09:00")
    available_time_end = models.TimeField(default="17:00")
    profile_image = models.CharField(max_length=200, default="/static/images/profilePhotos/doctor-avatar.png")  # Path to profile image
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    symptoms = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Appointment: {self.patient.first_name} with {self.doctor} on {self.appointment_date}"

# Create your models here.
