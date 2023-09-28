from django.db import models


# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    instructions = models.CharField(max_length=1000)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.name
    
    

class ingredients(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    quantity_type = models.CharField(max_length=50, default="")
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    def __str__ (self):
        return self.name