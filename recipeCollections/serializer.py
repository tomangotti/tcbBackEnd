from rest_framework import serializers

from recipes.models import Recipes
from django.contrib.auth.models import User
from .models import Collections



class CollectionSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipes.objects.all())

    class Meta:
        model = Collections
        fields = ('id', 'name', 'description', 'user', 'recipes',)