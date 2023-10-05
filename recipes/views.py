from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Recipes, ingredients
from .serializers import RecipesSerializer, IngredientsSerializer



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