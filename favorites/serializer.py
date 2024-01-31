from rest_framework import serializers

from recipes.models import Recipes
from django.contrib.auth.models import User
from .models import FavoriteRecipes, FavoriteCollections
from recipeCollections.models import Collections

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipes
        fields = ('id', 'user', 'recipe')

class FavoriteCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCollections
        fields = ('id', 'user', 'collection')
