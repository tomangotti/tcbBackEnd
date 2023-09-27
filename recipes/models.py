from django.db import models


# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    instructions = models.CharField(max_length=1000)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class ingredients(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)