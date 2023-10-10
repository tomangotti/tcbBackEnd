from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Recipes, ingredients, SavedRecipes
from .serializers import RecipesSerializer, IngredientsSerializer, SavedARecipeSerializer
from django.contrib.auth.models import User



class GetAllRecipes(APIView):
    serializer_class = RecipesSerializer

    def get(self, request, format=None):
        recipes = Recipes.objects.all()
        if len(recipes) > 0:
            serializer = RecipesSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class GetIngredients(APIView):
    serializer_class = IngredientsSerializer

    def get(self, request, code, format=None):
        recipe = get_object_or_404(Recipes, id=code)
        ingredients = recipe.ingredients_set.all()
        serializer = IngredientsSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class GetRecipeDetails(APIView):

    def get(self, request, code, format=None):
        recipe = get_object_or_404(Recipes, id=code)
        ingredients = recipe.ingredients_set.all()
        ingredients_serializer = IngredientsSerializer(ingredients, many=True)
        recipe_serializer = RecipesSerializer(recipe)
        data = {
            'ingredients': ingredients_serializer.data,
            'recipe': recipe_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    


class GetUserSavedRecipes(APIView):

    def get(self, request, code, format=None):
        user = get_object_or_404(User, id=code)
        saved_recipes = user.savedrecipes_set.all()
        recipe_list = [saved_recipe.recipe for saved_recipe in saved_recipes]
        serializer = RecipesSerializer(recipe_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    
    
    

class PostASavedRecipe(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = SavedARecipeSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            user = validated_data['user']
            recipe = validated_data['recipe']

            if User.objects.filter(id=user.id).exists() and Recipes.objects.filter(id=recipe.id).exists():
                newSavedRecipe = SavedRecipes(user=user, recipe=recipe)
                newSavedRecipe.save()
                return Response({'message': 'Recipe saved successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User or recipe does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


