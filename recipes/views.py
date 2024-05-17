from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction
from django.db.models import Avg

import json
import random
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import Recipes, ingredients, SavedRecipes, Cart, Tags, ratings
from .serializers import  CartSerializer, RecipesSerializer, IngredientsSerializer, SavedARecipeSerializer, SavedUsersSerializer, TagsSerializer, RatingsSerializer
from django.contrib.auth.models import User
from recipeCollections.models import Collections, CollectionRating
from social.models import Follow
from favorites.models import FavoriteRecipes, FavoriteCollections
from recipeCollections.serializer import CollectionSerializer, CollectionRatingSerializer
from ususers.models import User, ProfileImage
from ususers.serializers import QuickGlanceSerializer



class GetAllRecipes(APIView):
    serializer_class = RecipesSerializer

    def get(self, request, format=None):
        recipes = Recipes.objects.all().filter(published=True)
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

        return Response(serializer_data, status=status.HTTP_200_OK)




class GetFeedRecipes(APIView):
    serializer_class = RecipesSerializer

    def get_most_recent_recipes(self):
        date_14_days_ago = datetime.now() - timedelta(days=14)
        return Recipes.objects.filter(published=True, created_at__gte=date_14_days_ago).order_by('-created_at')[:10]
        
    
    def get_most_favorited_recipes(self):
        return(
            Recipes.objects.annotate(favorite_count=Count('recipe')).filter(published=True)
            .order_by('-favorite_count')[:10]
        )
    
    def get_highest_rated_recipes(self):
        return(
            Recipes.objects.annotate(avg_rating=Avg('ratings__rating')).filter(published=True)
            .order_by('-avg_rating')[:10]
        )
    
    def get_recipes_made_by_followed_users(self, user):
        followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        return Recipes.objects.filter(user__in=followed_users).filter(published=True).order_by('-created_at')[:10]

    def get_most_recent_collections(self):
        date_14_days_ago = datetime.now() - timedelta(days=21)
        return Collections.objects.filter(published=True, created_at__gte=date_14_days_ago).order_by('-created_at')[:10]
    
    def get_most_favorited_collections(self):
        return(
            Collections.objects.annotate(favorite_count=Count('collection')).filter(published=True)
            .order_by('-favorite_count')[:10]
        )
    
    def get_highest_rated_collections(self):
        return(
            Collections.objects.annotate(rating_count=Count('ratings')).filter(published=True)
            .order_by('-rating_count')[:10]
        )
    
    
    def get_collections_made_by_followed_users(self, user):
        followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        return Collections.objects.filter(user__in=followed_users).filter(published=True).order_by('-created_at')[:10]

    def get(self, request, user_id):
        most_recent_recipes = self.get_most_recent_recipes()
        most_favorited_recipes = self.get_most_favorited_recipes()
        highest_rated_recipes = self.get_highest_rated_recipes()
        recipes_made_by_followed_users = self.get_recipes_made_by_followed_users(user_id)
        
        most_recent_collections = self.get_most_recent_collections()
        most_favorited_collections = self.get_most_favorited_collections()
        highest_rated_collections = self.get_highest_rated_collections()
        collections_made_by_followed_users = self.get_collections_made_by_followed_users(user_id)

        

        most_recent_serializer = RecipesSerializer(most_recent_recipes, many=True)
        most_favorited_serializer = RecipesSerializer(most_favorited_recipes, many=True)
        highest_rated_serializer = RecipesSerializer(highest_rated_recipes, many=True)
        recipes_made_by_followed_users_serializer = RecipesSerializer(recipes_made_by_followed_users, many=True)

        most_recent_collections_serializer = CollectionSerializer(most_recent_collections, many=True)
        most_favorited_collections_serializer = CollectionSerializer(most_favorited_collections, many=True)
        highest_rated_collections_serializer = CollectionSerializer(highest_rated_collections, many=True)
        collections_made_by_followed_users_serializer = CollectionSerializer(collections_made_by_followed_users, many=True)

        

        most_recent_data = most_recent_serializer.data
        most_favorited_data = most_favorited_serializer.data
        highest_rated_data = highest_rated_serializer.data
        recipes_made_by_followed_users_data = recipes_made_by_followed_users_serializer.data

        most_recent_collections_data = most_recent_collections_serializer.data
        most_favorited_collections_data = most_favorited_collections_serializer.data
        highest_rated_collections_data = highest_rated_collections_serializer.data
        collections_made_by_followed_users_data = collections_made_by_followed_users_serializer.data

        

        for recipe_data in most_recent_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        
        for recipe_data in most_favorited_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass

        for recipe_data in highest_rated_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        
        for recipe_data in recipes_made_by_followed_users_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        

        


        data = [
            {'name': "Popular Recipes", 'data': most_favorited_data},
            {'name': "New Recipes", 'data': most_recent_data},
            {'name': "Recipes By Favorite Users", 'data': recipes_made_by_followed_users_data},
            {'name': "Popular Collections", 'data': most_favorited_collections_data},
            {'name': "Top Rated Recipes", 'data': highest_rated_data},
            {'name': "New Collections", 'data': most_recent_collections_data},
            {'name': "Top Rated Collections", 'data': highest_rated_collections_data},
            {'name': "Collections By Favorite Users", 'data': collections_made_by_followed_users_data},
        ]

        data = [item for item in data if item['data']]

        return Response(data, status=status.HTTP_200_OK)
    



class GetFeedRecipesV2(APIView):
    serializer_class = RecipesSerializer

    def get_most_recent_recipes(self):
        date_14_days_ago = datetime.now() - timedelta(days=14)
        return Recipes.objects.filter(published=True, created_at__gte=date_14_days_ago).order_by('-created_at')[:10]
        
    
    def get_most_favorited_recipes(self):
        return(
            Recipes.objects.annotate(favorite_count=Count('recipe')).filter(published=True)
            .order_by('-favorite_count')[:10]
        )
    
    def get_highest_rated_recipes(self):
        return(
            Recipes.objects.annotate(avg_rating=Avg('ratings__rating')).filter(published=True)
            .order_by('-avg_rating')[:10]
        )
    
    def get_recipes_made_by_followed_users(self, user):
        followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        return Recipes.objects.filter(user__in=followed_users).filter(published=True).order_by('-created_at')[:10]

    def get_most_recent_collections(self):
        date_14_days_ago = datetime.now() - timedelta(days=21)
        return Collections.objects.filter(published=True, created_at__gte=date_14_days_ago).order_by('-created_at')[:10]
    
    def get_most_favorited_collections(self):
        return(
            Collections.objects.annotate(favorite_count=Count('collection')).filter(published=True)
            .order_by('-favorite_count')[:10]
        )
    
    def get_highest_rated_collections(self):
        return(
            Collections.objects.annotate(rating_count=Count('ratings')).filter(published=True)
            .order_by('-rating_count')[:10]
        )
    
    def get_not_following_users(self, user, count=5):
        not_following_users = User.objects.exclude(following__follower=user)
    
        total_users = not_following_users.count()
        if total_users <= count:
            return not_following_users
        
        random_users = random.sample(list(not_following_users), count)
        return random_users





    def get_collections_made_by_followed_users(self, user):
        followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        return Collections.objects.filter(user__in=followed_users).filter(published=True).order_by('-created_at')[:10]

    def get(self, request, user_id):
        most_recent_recipes = self.get_most_recent_recipes()
        most_favorited_recipes = self.get_most_favorited_recipes()
        highest_rated_recipes = self.get_highest_rated_recipes()
        recipes_made_by_followed_users = self.get_recipes_made_by_followed_users(user_id)
        
        most_recent_collections = self.get_most_recent_collections()
        most_favorited_collections = self.get_most_favorited_collections()
        highest_rated_collections = self.get_highest_rated_collections()
        collections_made_by_followed_users = self.get_collections_made_by_followed_users(user_id)

        
        not_following_users = self.get_not_following_users(user_id)
        

        most_recent_serializer = RecipesSerializer(most_recent_recipes, many=True)
        most_favorited_serializer = RecipesSerializer(most_favorited_recipes, many=True)
        highest_rated_serializer = RecipesSerializer(highest_rated_recipes, many=True)
        recipes_made_by_followed_users_serializer = RecipesSerializer(recipes_made_by_followed_users, many=True)

        most_recent_collections_serializer = CollectionSerializer(most_recent_collections, many=True)
        most_favorited_collections_serializer = CollectionSerializer(most_favorited_collections, many=True)
        highest_rated_collections_serializer = CollectionSerializer(highest_rated_collections, many=True)
        collections_made_by_followed_users_serializer = CollectionSerializer(collections_made_by_followed_users, many=True)

        not_following_users_serializer = QuickGlanceSerializer(not_following_users, many=True)
        

        most_recent_data = most_recent_serializer.data
        most_favorited_data = most_favorited_serializer.data
        highest_rated_data = highest_rated_serializer.data
        recipes_made_by_followed_users_data = recipes_made_by_followed_users_serializer.data

        most_recent_collections_data = most_recent_collections_serializer.data
        most_favorited_collections_data = most_favorited_collections_serializer.data
        highest_rated_collections_data = highest_rated_collections_serializer.data
        collections_made_by_followed_users_data = collections_made_by_followed_users_serializer.data

        not_following_users_data = not_following_users_serializer.data
        

        for recipe_data in most_recent_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        
        for recipe_data in most_favorited_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass

        for recipe_data in highest_rated_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        
        for recipe_data in recipes_made_by_followed_users_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        

        for user_data in not_following_users_data:
            user_id = user_data['id']
            try:
                user = User.objects.get(pk=user_id)
                if ProfileImage.objects.filter(user=user):
                    profile_image = ProfileImage.objects.get(user=user)
                    if profile_image.image:
                        image_url = request.build_absolute_uri(profile_image.image.url)
                        user_data['image'] = image_url
            except User.DoesNotExist:
                pass


        data = [
            {'name': "Popular Recipes", 'data': most_favorited_data},
            {'name': "New Recipes", 'data': most_recent_data},
            {'name': "Recipes By Favorite Users", 'data': recipes_made_by_followed_users_data},
            {'name': "Popular Collections", 'data': most_favorited_collections_data},
            {'name': "Users to Follow", 'data': not_following_users_data},
            {'name': "Top Rated Recipes", 'data': highest_rated_data},
            {'name': "New Collections", 'data': most_recent_collections_data},
            {'name': "Top Rated Collections", 'data': highest_rated_collections_data},
            {'name': "Collections By Favorite Users", 'data': collections_made_by_followed_users_data},
        ]

        data = [item for item in data if item['data']]

        return Response(data, status=status.HTTP_200_OK)
    








class GetSlimFeedRecipes(APIView):
    serializer_class = RecipesSerializer

    def get_most_recent_recipes(self):
        date_14_days_ago = datetime.now() - timedelta(days=14)
        return Recipes.objects.filter(published=True, created_at__gte=date_14_days_ago).order_by('-created_at')[:10]
        
    
    def get_most_favorited_recipes(self):
        return(
            Recipes.objects.annotate(favorite_count=Count('recipe')).filter(published=True)
            .order_by('-favorite_count')[:10]
        )
    
    def get_highest_rated_recipes(self):
        return(
            Recipes.objects.annotate(avg_rating=Avg('ratings__rating')).filter(published=True)
            .order_by('-avg_rating')[:10]
        )

    def get_most_recent_collections(self):
        date_14_days_ago = datetime.now() - timedelta(days=21)
        return Collections.objects.filter(published=True, created_at__gte=date_14_days_ago).order_by('-created_at')[:10]
    
    def get_most_favorited_collections(self):
        return(
            Collections.objects.annotate(favorite_count=Count('collection')).filter(published=True)
            .order_by('-favorite_count')[:10]
        )
    
    def get_highest_rated_collections(self):
        return(
            Collections.objects.annotate(rating_count=Count('ratings')).filter(published=True)
            .order_by('-rating_count')[:10]
        )
    

    def get(self, request):
        most_recent_recipes = self.get_most_recent_recipes()
        most_favorited_recipes = self.get_most_favorited_recipes()
        highest_rated_recipes = self.get_highest_rated_recipes()
        most_recent_collections = self.get_most_recent_collections()
        most_favorited_collections = self.get_most_favorited_collections()
        highest_rated_collections = self.get_highest_rated_collections()

        most_recent_serializer = RecipesSerializer(most_recent_recipes, many=True)
        most_favorited_serializer = RecipesSerializer(most_favorited_recipes, many=True)
        highest_rated_serializer = RecipesSerializer(highest_rated_recipes, many=True)

        most_recent_collections_serializer = CollectionSerializer(most_recent_collections, many=True)
        most_favorited_collections_serializer = CollectionSerializer(most_favorited_collections, many=True)
        highest_rated_collections_serializer = CollectionSerializer(highest_rated_collections, many=True)

        most_recent_data = most_recent_serializer.data
        most_favorited_data = most_favorited_serializer.data
        highest_rated_data = highest_rated_serializer.data

        most_recent_collections_data = most_recent_collections_serializer.data
        most_favorited_collections_data = most_favorited_collections_serializer.data
        highest_rated_collections_data = highest_rated_collections_serializer.data

        for recipe_data in most_recent_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        
        for recipe_data in most_favorited_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass

        for recipe_data in highest_rated_data:
            recipe_id = recipe_data['id']
            try:
                recipe = Recipes.objects.get(pk=recipe_id)
                if recipe.image:
                    image_url = request.build_absolute_uri(recipe.image.url)
                    recipe_data['image'] = image_url
            except Recipes.DoesNotExist:
                pass
        
        
        
        data = [
            {'name': "New Recipes", 'data': most_recent_data},
            {'name': "Popular Recipes", 'data': most_favorited_data},
            {'name': "Popular Collections", 'data': most_favorited_collections_data},
            {'name': "Highest Rated Recipes", 'data': highest_rated_data},
            {'name': "New Collections", 'data': most_recent_collections_data},
            {'name': "Highest Rated Collections", 'data': highest_rated_collections_data},
        ]

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
        print(request.data)
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
            published = validated_data['published']

            if 'image' in validated_data:
                image = validated_data['image']
            else:
                image = None  

            newRecipe = Recipes(name=name, description=description, instructions=instructions, image=image, user=user, category=category, servings=servings, cook_time=cook_time, published=published)
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
            recipe.published = serializer.validated_data['published']

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
    

class AddNewRatingView(APIView):
    serializer_class = RatingsSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = RatingsSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            recipe_id = validated_data['recipe']
            user_id = validated_data['user']
            rating_value = validated_data['rating']

            print(recipe_id)
            print(user_id)
            print(rating_value)

            if ratings.objects.filter(recipe=recipe_id, user=user_id):
                oldrating = ratings.objects.filter(recipe=recipe_id, user=user_id)
                oldrating.delete()
                
            rating = ratings(recipe=recipe_id, user=user_id, rating=rating_value)
            rating.save()
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
            

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetUsersRecipeRating(APIView):
    serializer_class = RatingsSerializer

    def get(self, request, user_id, recipe_id, format=None):

        if ratings.objects.filter(recipe=recipe_id, user=user_id).exists():
            rating = ratings.objects.get(recipe=recipe_id, user=user_id)
            serializer = RatingsSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response({'message': 'No rating found'}, status=status.HTTP_200_OK)
        
    



# new recipe classes
    
class GetUsersRecipes(APIView):
    serializer_class = RecipesSerializer

    def get(self, request, code, format=None):
        user = get_object_or_404(User, id=code)
        
        recipes = user.recipes_set.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)