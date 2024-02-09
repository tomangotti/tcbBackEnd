from rest_framework import serializers

from recipes.models import Recipes
from recipes.serializers import RecipesSerializer
from django.contrib.auth.models import User
from .models import Collections


class CollectionSerializer(serializers.ModelSerializer):
    recipes = RecipesSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Collections
        fields = ('id', 'name', 'description', 'user', 'recipes', 'user_username')