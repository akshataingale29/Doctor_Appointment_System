from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        print(f"EmailBackend authenticate called with username: {username}")
        
        try:
            # Try to get user by email (username is actually email in our case)
            user = UserModel.objects.get(email=username)
            print(f"User found with email {username}")
            
            if user.check_password(password):
                print(f"Password check successful for {username}")
                return user
            else:
                print(f"Password check failed for {username}")
                return None
                
        except UserModel.DoesNotExist:
            print(f"No user found with email {username}")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            print(f"get_user retrieved user with ID: {user_id}, email: {user.email}")
            return user
        except UserModel.DoesNotExist:
            print(f"get_user failed: no user with ID {user_id}")
            return None 