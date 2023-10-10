from rest_framework import serializers
from .models import Recipes, ingredients, SavedRecipes

class RecipesSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only="true")

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'description', 'instructions', 'published', 'user_username', 'user' )


class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ingredients
        fields = ('id', 'name', 'quantity', 'quantity_type')

class SavedARecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipes
        fields = ('user', 'recipe')
        extra_kwargs = {'user': {'required': False}}

