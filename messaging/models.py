from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Messages(models.Model):
    content = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default="")

    def __str__ (self):
        return self.content