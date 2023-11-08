from rest_framework import serializers
from .models import Recipes, ingredients, SavedRecipes, Cart

# 

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredients
        fields = ('id', 'name', 'quantity', 'quantity_type')

class RecipesSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'description', 'instructions', 'published', 'user_username', 'user', 'image', 'ingredients')

    def get_image_url(self, obj):
        if obj.image:
            # Assuming you have MEDIA_URL configured in your settings
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None



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
