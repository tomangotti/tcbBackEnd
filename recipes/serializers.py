from rest_framework import serializers
from .models import Recipes, ingredients, SavedRecipes, Cart, Tags, ratings

# 

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredients
        fields = ('id', 'name', 'quantity', 'quantity_type')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name', 'recipe')

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ratings
        fields = ('rating', 'recipe', 'user')


class RecipesSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    ratings = RatingsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'description', 'instructions', 'published', 'user_username', 'user', 'image', 'ingredients', 'category', 'servings', 'cook_time', 'tags', 'ratings')





class SavedARecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipes
        fields = ('user', 'recipe')
        extra_kwargs = {'user': {'required': False}}

class SavedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipes
        fields = ('user',) 
        extra_kwargs = {'user': {'required': False}}

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')


