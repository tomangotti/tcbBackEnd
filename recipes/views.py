from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Recipes, ingredients, SavedRecipes
from .serializers import RecipesSerializer, IngredientsSerializer, SavedARecipeSerializer, SavedUsersSerializer
from django.contrib.auth.models import User



class GetAllRecipes(APIView):
    serializer_class = RecipesSerializer

    def get(self, request, format=None):
        recipes = Recipes.objects.all()
        if len(recipes) > 0:
            serializer = RecipesSerializer(recipes, many=True)
            serializer_data = serializer.data

            for recipe_data in serializer_data:
                recipe_id = recipe_data['id']
                try:
                    recipe = Recipes.objects.get(pk=recipe_id)
                    if recipe.image:
                        image_url = request.build_absolute_uri(recipe.image.url)
                        recipe_data['image'] = image_url
                except Recipes.DoesNotExist:
                    pass
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
        saved_users = recipe.savedrecipes_set.all()
        ingredients_serializer = IngredientsSerializer(ingredients, many=True)
        recipe_serializer = RecipesSerializer(recipe)
        recipe_data = recipe_serializer.data
        saved_user_serializer = SavedUsersSerializer(saved_users, many=True)
        recipe_id = recipe_data["id"]
        try:
            recipe=Recipes.objects.get(pk=recipe_id)
            if recipe.image:
                image_url = request.build_absolute_uri(recipe.image.url)
                recipe_data['image'] = image_url
        except Recipes.DoesNotExist:
            pass
        data = {
            'ingredients': ingredients_serializer.data,
            'recipe': recipe_data,
            'users': saved_user_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    


class GetUserSavedRecipes(APIView):

    def get(self, request, code, format=None):
        user = get_object_or_404(User, id=code)
        saved_recipes = user.savedrecipes_set.all()
        recipe_list = [saved_recipe.recipe for saved_recipe in saved_recipes]
        serializer = RecipesSerializer(recipe_list, many=True)
        serializer_data = serializer.data

        for recipe_data in serializer_data:
                recipe_id = recipe_data['id']
                try:
                    recipe = Recipes.objects.get(pk=recipe_id)
                    if recipe.image:
                        image_url = request.build_absolute_uri(recipe.image.url)
                        recipe_data['image'] = image_url
                except Recipes.DoesNotExist:
                    pass

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostNewRecipe(APIView):

    def post(self, request, *args, **kwargs):
        
        recipe_serializer = RecipesSerializer(data=request.data)

        if recipe_serializer.is_valid():
            # Extract data from the recipe
            validated_data = recipe_serializer.validated_data
            name = validated_data['name']
            description = validated_data['description']
            instructions = validated_data['instructions']
            image = validated_data['image']
            user = validated_data['user']

            # Create a new recipe
            newRecipe = Recipes(name=name, description=description, instructions=instructions, image=image, user=user)
            newRecipe.save()

            # Extract ingredients data from the request
            ingredients_data = json.loads(request.data.get('ingredients', '[]'))  # Parse the JSON string
            print(ingredients_data)
            # Now you can process and save ingredients if necessary
            for ingredient_data in ingredients_data:
                print(ingredient_data)
                ingredient = ingredients(
                    recipe=newRecipe,
                    name=ingredient_data['name'],
                    quantity=ingredient_data['quantity'],
                    quantity_type=ingredient_data['quantity_type']
                )
                ingredient.save()
                
            newSavedRecipe = SavedRecipes(user=user, recipe=newRecipe)
            newSavedRecipe.save()

            return Response({'message': 'Recipe and ingredients added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            print(recipe_serializer.error_messages)
            return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    

class  AddOrRemoveSavedRecipeList(APIView):
    
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
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        serializer = SavedARecipeSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = validated_data['user']
            recipe = validated_data['recipe']

            if SavedRecipes.objects.filter(user=user, recipe=recipe):
                deleteRecipe = SavedRecipes.objects.filter(user=user, recipe=recipe)
                deleteRecipe.delete()
                return Response({'message': 'Recipe remove successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User or recipe does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
