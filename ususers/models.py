from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    def __str__(self):
        return self.email
    
    groups = models.ManyToManyField(
            'auth.Group',
            related_name='custom_user_groups',
            blank=True,
        )
        
    user_permissions = models.ManyToManyField(
            'auth.Permission',
            related_name='custom_user_user_permissions',
            blank=True,
        )