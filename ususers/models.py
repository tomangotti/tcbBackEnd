from django.db import models
from django.contrib.auth.models import User

class RandomCode(models.Model):
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.code