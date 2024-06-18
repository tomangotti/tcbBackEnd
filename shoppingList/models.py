from django.db import models
from recipes.models import Recipes
from django.contrib.auth.models import User

# Create your models here.


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_list')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe.name
    

class ListItems(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='list_items', blank=True)
    quantity = models.CharField(max_length=50, blank=True)
    quantity_type = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100, blank=True)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe.name
    

class SharedLists(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='shared_list')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_lists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shopping