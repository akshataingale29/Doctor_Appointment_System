import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from members.models import Speciality

# Define the specialty to image mappings
specialty_images = {
    'Cancer Care': '/static/images/cancer-ribbon-clipart-teal-7.png',
    'Fertility & IVF': '/static/images/fertility.png',
    'Pulmonology': '/static/images/lungtransplant.png',
    'Neurology': '/static/images/neurology.png'
}

# Update the image paths in the database
updated_count = 0
for specialty_name, image_path in specialty_images.items():
    try:
        specialty = Speciality.objects.get(name=specialty_name)
        specialty.image = image_path
        specialty.save()
        print(f"Updated {specialty_name} with image path: {image_path}")
        updated_count += 1
    except Speciality.DoesNotExist:
        print(f"Specialty '{specialty_name}' not found in database")

print(f"\nTotal specialties updated: {updated_count}") 