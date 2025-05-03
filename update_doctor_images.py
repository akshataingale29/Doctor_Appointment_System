import os
import django
import glob
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from members.models import Doctor

User = get_user_model()

def get_available_doctor_images():
    """Get a list of all available doctor profile images"""
    image_dir = os.path.join("static", "images", "profilePhotos")
    image_files = glob.glob(os.path.join(image_dir, "*.png"))
    return [os.path.basename(f) for f in image_files]

def find_matching_image(first_name, last_name, available_images):
    """Find the best matching image for a doctor"""
    if not first_name or not last_name:
        return None
        
    clean_first = first_name.strip().replace(" ", "")
    clean_last = last_name.strip().replace(" ", "")
    
    # Try exact match first
    exact_match = f"Dr{clean_first}{clean_last}.png"
    if exact_match in available_images:
        return f"/static/images/profilePhotos/{exact_match}"
    
    # Try partial matches
    for img in available_images:
        if img.startswith(f"Dr{clean_first}") or (clean_last and img.startswith(f"Dr") and clean_last in img):
            return f"/static/images/profilePhotos/{img}"
    
    # Default to doctor-avatar.png if no match found
    return "/static/images/profilePhotos/doctor-avatar.png"

def main():
    # Get list of available doctor images
    available_images = get_available_doctor_images()
    print(f"Found {len(available_images)} doctor profile images")
    
    print("\nUpdating doctor profile images...")
    for doctor in Doctor.objects.all():
        first_name = doctor.user.first_name
        last_name = doctor.user.last_name
        
        old_image = doctor.profile_image
        
        # Get new image path based on available images
        new_image_path = find_matching_image(first_name, last_name, available_images)
        
        if new_image_path:
            # Update the doctor's profile image
            doctor.profile_image = new_image_path
            doctor.save()
            
            print(f"Updated Dr. {first_name} {last_name}: {old_image} -> {new_image_path}")
        else:
            print(f"No matching image found for Dr. {first_name} {last_name}")
    
    print("\nAfter updates:")
    print("--------------")
    for doctor in Doctor.objects.all():
        print(f"Dr. {doctor.user.first_name} {doctor.user.last_name}")
        print(f"Profile Image: {doctor.profile_image}")
        print()

# Define the doctor to image mappings (by doctor ID and name)
doctor_images = {
    1: '/static/images/ProfilePhotos/DrRajeshSharma.jpeg',  # Dr. Rajesh Sharma
    7: '/static/images/ProfilePhotos/DrAmitRGupta.png',     # Dr. Amit R Gupta
    10: '/static/images/ProfilePhotos/DrAatishShah.jpeg'    # Dr. Aatish Shah
}

# Update the image paths in the database
updated_count = 0
for doctor_id, image_path in doctor_images.items():
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        old_path = doctor.profile_image
        doctor.profile_image = image_path
        doctor.save()
        print(f"Updated Dr. {doctor.user.first_name} {doctor.user.last_name}")
        print(f"  Old path: {old_path}")
        print(f"  New path: {image_path}")
        updated_count += 1
    except Doctor.DoesNotExist:
        print(f"Doctor with ID {doctor_id} not found in database")

print(f"\nTotal doctors updated: {updated_count}")

if __name__ == "__main__":
    main() 