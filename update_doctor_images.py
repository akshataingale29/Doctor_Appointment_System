import os
import django
import glob

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from members.models import Doctor

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

if __name__ == "__main__":
    main() 