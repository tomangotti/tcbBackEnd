from rest_framework import serializers
from django.shortcuts import get_object_or_404

from recipes.models import Recipes
from recipes.serializers import RecipesSerializer
from django.contrib.auth.models import User
from .models import Collections


class CollectionSerializer(serializers.ModelSerializer):
    recipes = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Recipes.objects.all()),
        write_only=True
    )
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Collections
        fields = ('id', 'name', 'description', 'user', 'recipes', 'user_username')

    def create(self, validated_data):
        recipes_data = validated_data.pop('recipes', [])
        collection = Collections.objects.create(**validated_data)

        for recipe_id in recipes_data:
            recipe = get_object_or_404(Recipes, pk=recipe_id.pk)
            collection.recipes.add(recipe)

        return collection