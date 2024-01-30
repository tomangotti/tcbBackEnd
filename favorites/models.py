from django.db import models
from recipes.models import Recipes
from django.contrib.auth.models import User
from recipeCollections.models import Collections
# Create your models here.


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='recipe')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.name
    

class FavoriteCollections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_collection')
    collection = models.ForeignKey(Collections, on_delete=models.CASCADE, related_name='collection')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.name