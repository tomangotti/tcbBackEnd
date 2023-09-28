from rest_framework import serializers
from .models import Recipes, ingredients

class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'description', 'instructions', 'published' )


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredients
        fields = ('id', 'name', 'quantity', 'quantity_type')