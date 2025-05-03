import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from members.models import Doctor

def check_file_exists(filepath):
    """Check if the file exists, removing the leading / from the path"""
    if filepath.startswith('/'):
        filepath = filepath[1:]
    return os.path.exists(filepath)

def main():
    print("Doctors and their profile images:")
    print("---------------------------------")
    for doctor in Doctor.objects.all():
        first_name = doctor.user.first_name
        last_name = doctor.user.last_name
        image_path = doctor.profile_image
        
        # Check if the file exists
        file_exists = check_file_exists(image_path)
        status = "✓ EXISTS" if file_exists else "✗ MISSING"
        
        print(f"Dr. {first_name} {last_name}")
        print(f"Profile Image: {image_path} [{status}]")
        print()

if __name__ == "__main__":
    main() 