import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from members.models import Doctor

# Define the doctor image updates
updates = [
    # doctor_id, new_image_path
    (1, '/static/images/ProfilePhotos/DrRajeshSharma.jpeg'),  # Dr. Rajesh Sharma
    (7, '/static/images/ProfilePhotos/DrAmitRGupta.png'),     # Dr. Amit R Gupta
    (10, '/static/images/ProfilePhotos/DrAatishShah.jpeg')    # Dr. Aatish Shah
]

# Print current state
print("Current image paths:")
for doctor_id, _ in updates:
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        print(f"{doctor_id}. Dr. {doctor.user.first_name} {doctor.user.last_name} - {doctor.profile_image}")
    except Doctor.DoesNotExist:
        print(f"Doctor with ID {doctor_id} not found")

print("\nUpdating image paths...")

# Update image paths
for doctor_id, new_path in updates:
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        old_path = doctor.profile_image
        doctor.profile_image = new_path
        doctor.save()
        print(f"Updated Dr. {doctor.user.first_name} {doctor.user.last_name}")
        print(f"  From: {old_path}")
        print(f"  To:   {new_path}")
    except Doctor.DoesNotExist:
        print(f"Error: Doctor with ID {doctor_id} not found")

# Verify updated state
print("\nVerifying updates:")
for doctor_id, _ in updates:
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        print(f"{doctor_id}. Dr. {doctor.user.first_name} {doctor.user.last_name} - {doctor.profile_image}")
    except Doctor.DoesNotExist:
        print(f"Doctor with ID {doctor_id} not found")

print("\nUpdate complete!") 