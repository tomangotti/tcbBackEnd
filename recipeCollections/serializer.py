from rest_framework import serializers
from django.shortcuts import get_object_or_404

from recipes.models import Recipes
from recipes.serializers import RecipesSerializer
from django.contrib.auth.models import User
from .models import Collections, CollectionRating

class CollectionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionRating
        fields = ('rating', 'collection', 'user')

class CollectionSerializer(serializers.ModelSerializer):
    recipes_details = RecipesSerializer(source='recipes', many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    average_rating = serializers.ReadOnlyField()
    published = serializers.BooleanField(required=False)
    class Meta:
        model = Collections
        fields = ('id', 'name', 'description', 'user', 'recipes', 'user_username', 'recipes_details', 'average_rating', 'published')

