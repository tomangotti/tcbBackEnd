from django.db import models
from recipes.models import Recipes
from django.contrib.auth.models import User


class Collections(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    recipes = models.ManyToManyField(Recipes,related_name='collections', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__ (self):
        return self.name

