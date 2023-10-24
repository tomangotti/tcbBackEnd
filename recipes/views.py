from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count


import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Recipes, ingredients, SavedRecipes, Cart
from .serializers import  CartSerializer, RecipesSerializer, IngredientsSerializer, SavedARecipeSerializer, SavedUsersSerializer
from django.contrib.auth.models import User


class GetAllRecipes(APIView):
    serializer_class = RecipesSerializer

    def get_most_recent_recipes(self):
        return Recipes.objects.order_by('-created_at')[:10]

    def get_most_saved_recipes(self):
        return (
            Recipes.objects.annotate(saved_count=Count('savedrecipes'))
            .order_by('-saved_count')[:10]
        )

    def get(self, request, format=None):
        most_recent_recipes = self.get_most_recent_recipes()
        most_saved_recipes = self.get_most_saved_recipes()

        most_recent_serializer = RecipesSerializer(most_recent_recipes, many=True)
        most_saved_serializer = RecipesSerializer(most_saved_recipes, many=True)

        most_recent_data = most_recent_serializer.data
        most_saved_data = most_saved_serializer.data

        for recipe_data in most_recent_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass

        for recipe_data in most_saved_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass

        data = {
            'most_recent_recipes': most_recent_data,
            'most_saved_recipes': most_saved_data,
        }

        return Response(data, status=status.HTTP_200_OK)

# class GetAllRecipes(APIView):
#     serializer_class = RecipesSerializer
#     def get(self, request, format=None):
#         recipes = Recipes.objects.all()
#         if len(recipes) > 0:
#             serializer = RecipesSerializer(recipes, many=True)
#             serializer_data = serializer.data

#             for recipe_data in serializer_data:
#                 recipe_id = recipe_data['id']
#                 try:
#                     recipe = Recipes.objects.get(pk=recipe_id)
#                     if recipe.image:
#                         image_url = request.build_absolute_uri(recipe.image.url)
#                         recipe_data['image'] = image_url
#                 except Recipes.DoesNotExist:
#                     pass
#             return Response(serializer.data, status=status.HTTP_200_OK)



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
        
        # Use the IngredientsSerializer to serialize ingredients
        ingredients_serializer = IngredientsSerializer(recipe.ingredients.all(), many=True)
        
        # Use the SavedUsersSerializer to serialize saved users
        saved_user_serializer = SavedUsersSerializer(recipe.savedrecipes_set.all(), many=True)
        
        # Use the RecipesSerializer to serialize the recipe
        recipe_serializer = RecipesSerializer(recipe)
        
        # Serialize the recipe data
        recipe_data = recipe_serializer.data
        
        # Check and update the image URL if it exists
        if recipe.image:
            image_url = request.build_absolute_uri(recipe.image.url)
            recipe_data['image'] = image_url
        
        # Create a response data dictionary
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
            validated_data = recipe_serializer.validated_data
            name = validated_data['name']
            description = validated_data['description']
            instructions = validated_data['instructions']
            image = validated_data['image']
            user = validated_data['user']

        
            newRecipe = Recipes(name=name, description=description, instructions=instructions, image=image, user=user)
            newRecipe.save()

           
            ingredients_data = json.loads(request.data.get('ingredients', '[]'))  
            
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
    


class DeleteRecipeView(APIView):
    serializer_class = RecipesSerializer

    def delete(self, request, *args, **kwargs):
        serializer = RecipesSerializer(data=request.data)



class GetUserCartView(APIView):
    serializer_class = CartSerializer

    def get(self, request, code, format=None):
        user = get_object_or_404(User, id=code)
        cart_items = user.cart_set.all()
        cart_list = [cart_item.recipe for cart_item in cart_items]
        serializer = RecipesSerializer(cart_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddRecipeToCartView(APIView):
    # serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            user = validated_data['user']
            recipe = validated_data['recipe']

            if User.objects.filter(id=user.id).exists() and Recipes.objects.filter(id=recipe.id).exists():
                newCartItem = Cart(user=user, recipe=recipe)
                newCartItem.save()
                return Response({'message': 'Recipe added to Cart successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'User or recipe does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RemoveRecipeFromCartView(APIView):
    serializer_class = CartSerializer

    def delete(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            user = validated_data['user']
            recipe = validated_data['recipe']

            if Cart.objects.filter(user=user, recipe=recipe):
                cart_item = Cart.objects.filter(user=user, recipe=recipe)
                cart_item.delete()
                return Response({'message': 'Cart item removed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Cart Item did not exist'}, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

