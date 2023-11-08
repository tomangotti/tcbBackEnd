from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    instructions = models.CharField(max_length=1000)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=4)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)

    def __str__ (self):
        return self.name
    

    

class ingredients(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50, default="")
    quantity_type = models.CharField(max_length=50, default="")
    recipe = models.ForeignKey(Recipes, related_name='ingredients', on_delete=models.CASCADE)

    def __str__ (self):
        return self.name
    


class SavedRecipes(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
