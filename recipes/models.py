from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=750)
    instructions = models.CharField(max_length=10000)
    published = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=4)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    category = models.CharField(max_length=50, default="other", blank=True)
    servings = models.CharField(max_length=50, default="", blank=True)
    cook_time = models.CharField(max_length=50, default="", blank=True)

    def average_rating(self):
        all_ratings = ratings.objects.filter(recipe=self)
        if len(all_ratings) > 0:
            return sum([x.rating for x in all_ratings]) / len(all_ratings)
        else:
            return 0

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



class Tags(models.Model):
    name = models.CharField(max_length=50)
    recipe = models.ForeignKey(Recipes, related_name='tags', on_delete=models.CASCADE)

    def __str__ (self):
        return self.name
    

class ratings(models.Model):
    rating = models.IntegerField()
    recipe = models.ForeignKey(Recipes, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

