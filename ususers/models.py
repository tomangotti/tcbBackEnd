from django.db import models
from django.contrib.auth.models import User

class RandomCode(models.Model):
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    


class Links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    link_twitter = models.CharField(max_length=1000,blank=True, null=True)
    link_instagram = models.CharField(max_length=1000, blank=True, null=True)
    link_facebook = models.CharField(max_length=1000, blank=True, null=True)
    link_youtube = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.link



class ProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url