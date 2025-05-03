import os
import django
import shutil
import glob

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from members.models import Doctor, User

def check_file_exists(filepath):
    """Check if the file exists, removing the leading / from the path"""
    if not filepath:
        return False
    if filepath.startswith('/'):
        filepath = filepath[1:]
    return os.path.exists(filepath)

def create_default_avatar():
    """Create a default doctor avatar by copying an existing image"""
    default_path = "static/images/profilePhotos/doctor-avatar.png"
    
    # If the default image already exists, return its path
    if os.path.exists(default_path):
        return f"/{default_path}"
    
    # Find any existing doctor image to use as a fallback
    existing_images = glob.glob("static/images/profilePhotos/Dr*.png")
    if existing_images:
        # Copy the first found doctor image to the default avatar name
        source_img = existing_images[0]
        shutil.copy2(source_img, default_path)
        print(f"Created default avatar from {source_img}")
        return f"/{default_path}"
    
    # If no existing images, use a descriptive placeholder path
    return "/static/images/profilePhotos/doctor-avatar.png"

def main():
    print("Fixing doctor profile images...")
    
    # Create or ensure a default doctor avatar exists
    default_image = create_default_avatar()
    
    # Update all doctor records
    for doctor in Doctor.objects.all():
        first_name = doctor.user.first_name
        last_name = doctor.user.last_name
        current_image = doctor.profile_image
        
        # Fix empty or missing images
        if not current_image or not check_file_exists(current_image):
            doctor.profile_image = default_image
            doctor.save()
            print(f"Updated Dr. {first_name} {last_name}: {current_image} -> {default_image}")
    
    print("\nFinal Doctor Profile Image Status:")
    print("----------------------------------")
    for doctor in Doctor.objects.all():
        name = f"Dr. {doctor.user.first_name} {doctor.user.last_name}"
        image = doctor.profile_image
        file_exists = check_file_exists(image)
        status = "✓ EXISTS" if file_exists else "✗ MISSING"
        
        print(f"{name.ljust(30)} | {image} [{status}]")

if __name__ == "__main__":
    main() 