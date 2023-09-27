from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, name, password=None):
#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name)
#         user.set_password(password)  # Set the password
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=255)
#     password = models.CharField(max_length=128)  # Add a password field
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_admin = models.BooleanField(default=False)
    
