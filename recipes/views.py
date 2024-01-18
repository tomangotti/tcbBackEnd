from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction

import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Recipes, ingredients, SavedRecipes, Cart, Tags, ratings
from .serializers import  CartSerializer, RecipesSerializer, IngredientsSerializer, SavedARecipeSerializer, SavedUsersSerializer, TagsSerializer
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
        
        ingredients_serializer = IngredientsSerializer(recipe.ingredients.all(), many=True)
        
        saved_user_serializer = SavedUsersSerializer(recipe.savedrecipes_set.all(), many=True)
        
        recipe_serializer = RecipesSerializer(recipe)

        recipe_data = recipe_serializer.data
        
        if recipe.image:
            image_url = request.build_absolute_uri(recipe.image.url)
            recipe_data['image'] = image_url
        
        data = {
            'ingredients': ingredients_serializer.data,
            'recipe': recipe_data,
            'users': saved_user_serializer.data,
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
            user = validated_data['user']
            category = validated_data['category']
            servings = validated_data['servings']
            cook_time = validated_data['cook_time']


            if 'image' in validated_data:
                image = validated_data['image']
            else:
                image = None  

            newRecipe = Recipes(name=name, description=description, instructions=instructions, image=image, user=user, category=category, servings=servings, cook_time=cook_time)
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

            tag_data = json.loads(request.data.get('tags', '[]'))

            for tag in tag_data:
                newTag = Tags(name=tag, recipe=newRecipe)
                newTag.save()
                
            newSavedRecipe = SavedRecipes(user=user, recipe=newRecipe)
            newSavedRecipe.save()

            return Response({'message': 'Recipe and ingredients added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            print(recipe_serializer.error_messages)
            return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class  AddOrRemoveSavedRecipeList(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = SavedARecipeSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print('wearevalid')
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


class ShareRecipeWithUser(APIView):
    
    def post(self, request, code, *args, **kwargs):
        
        if User.objects.filter(email=request.data["email"]).exists() and Recipes.objects.filter(id=code).exists():
            user = User.objects.get(email=request.data["email"])
            recipe = Recipes.objects.get(id=code)

            newSavedRecipe = SavedRecipes(user=user, recipe=recipe)
            newSavedRecipe.save()
            return Response({'message': 'Recipe saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User or recipe does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
        

class EditRecipe(APIView):
    serializer_class = RecipesSerializer

    def patch(self, request, code, *args, **kwargs):

        recipe = get_object_or_404(Recipes, id=code)
        serializer = RecipesSerializer(recipe, data=request.data, partial=True)

        if serializer.is_valid():

            recipe.ingredients.all().delete()
            recipe.tags.all().delete()

            recipe.name = serializer.validated_data['name']
            recipe.description = serializer.validated_data['description']
            recipe.instructions = serializer.validated_data['instructions']
            recipe.category = serializer.validated_data['category']
            recipe.servings = serializer.validated_data['servings']
            recipe.cook_time = serializer.validated_data['cook_time']

            if 'image' in serializer.validated_data:
                recipe.image = serializer.validated_data['image']

            recipe.save()

            ingredients_data = json.loads(request.data.get('ingredients', '[]'))
            with transaction.atomic():
                for ingredient_data in ingredients_data:
                    ingredient = ingredients(
                        recipe=recipe,
                        name=ingredient_data['name'],
                        quantity=ingredient_data['quantity'],
                        quantity_type=ingredient_data['quantity_type']
                    )
                    ingredient.save()

            tag_data = json.loads(request.data.get('tags', '[]'))

            for tag in tag_data:
                newTag = Tags(name=tag, recipe=recipe)
                newTag.save()

            return Response({'message': 'Recipe updated successfully'}, status=status.HTTP_200_OK)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRecipe(APIView):
    def delete(self, request, code, *args, **kwargs):
        recipe = get_object_or_404(Recipes, id=code)
        recipe.delete()
        return Response({'message': 'Recipe deleted successfully'}, status=status.HTTP_200_OK)
    

# class GetAllInfo(APIView):
#     def get(self, request):
#         try:
#             recipe = Recipes.objects.all()
#             users = User.objects.all()
#             recipe_serializer = RecipesSerializer(recipe, many=True)
#             users_serializer = SavedUsersSerializer(users, many=True)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({'recipes': recipe_serializer.data, 'users': users_serializer.data}, status=status.HTTP_200_OK)