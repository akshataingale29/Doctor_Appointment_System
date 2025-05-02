from django.core.management.base import BaseCommand
from members.models import Doctor

class Command(BaseCommand):
    help = 'Updates doctor profile images based on their specialties'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to update doctor profile images...'))
        
        # Get all doctors
        doctors = Doctor.objects.all()
        updated_count = 0
        
        for doctor in doctors:
            # If doctor has a speciality and the speciality has an image
            if doctor.speciality and doctor.speciality.image:
                doctor.profile_image = doctor.speciality.image
                doctor.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Updated profile image for Dr. {doctor.user.first_name} {doctor.user.last_name} '
                    f'with {doctor.speciality.name} specialty image'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Skipped Dr. {doctor.user.first_name} {doctor.user.last_name} - '
                    'No specialty image available'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated {updated_count} doctor profile images!'
        )) 