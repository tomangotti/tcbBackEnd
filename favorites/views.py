from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from recipes.models import Recipes
from django.contrib.auth.models import User
from recipeCollections.models import Collections
from recipeCollections.serializer import CollectionSerializer
from .models import FavoriteRecipes, FavoriteCollections
from .serializer import FavoriteRecipeSerializer, FavoriteCollectionSerializer


# Create your views here.
class AddRecipeToFavorites(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get_recipe(self, recipe_id):
        return get_object_or_404(Recipes, pk=recipe_id)

    def post(self, request, user_id, recipe_id):
        user = self.get_user(user_id)
        recipe = self.get_recipe(recipe_id)
        favorite = FavoriteRecipes.objects.create(user=user, recipe=recipe)
        favorite.save()
        return Response(status=status.HTTP_200_OK)
    

class RemoveRecipeFromFavorites(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get_recipe(self, recipe_id):
        return get_object_or_404(Recipes, pk=recipe_id)

    def delete(self, request, user_id, recipe_id):
        user = self.get_user(user_id)
        recipe = self.get_recipe(recipe_id)
        favorite = FavoriteRecipes.objects.filter(user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_200_OK)
    

class AddCollectionToFavorites(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def post(self, request, user_id, collection_id):
        user = self.get_user(user_id)
        collection = self.get_collection(collection_id)
        favorite = FavoriteCollections.objects.create(user=user, collection=collection)
        favorite.save()
        return Response(status=status.HTTP_200_OK)
    
class RemoveCollectionFromFavorites(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def delete(self, request, user_id, collection_id):
        user = self.get_user(user_id)
        collection = self.get_collection(collection_id)
        favorite = FavoriteCollections.objects.filter(user=user, collection=collection)
        favorite.delete()
        return Response(status=status.HTTP_200_OK)
    

class GetUsersFavoriteRecipes(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        favorites = FavoriteRecipes.objects.filter(user=user)
        serializer = FavoriteRecipeSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetUsersFavoriteCollections(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        favorites = FavoriteCollections.objects.filter(user=user)
        list_collection = []
        for favorite in favorites:
            print(favorite.collection)
            collection = Collections.objects.get(pk=favorite.collection.id)
            list_collection.append(collection)
        serializer = CollectionSerializer(list_collection, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetSpecificFavoriteRecipeCheck(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get_recipe(self, recipe_id):
        return get_object_or_404(Recipes, pk=recipe_id)

    def get(self, request, user_id, recipe_id):
        user = self.get_user(user_id)
        recipe = self.get_recipe(recipe_id)
        favorite = FavoriteRecipes.objects.filter(user=user, recipe=recipe)
        if favorite:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class GetSpecificFavoriteCollectionCheck(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get(self, request, user_id, collection_id):
        user = self.get_user(user_id)
        collection = self.get_collection(collection_id)
        favorite = FavoriteCollections.objects.filter(user=user, collection=collection)
        if favorite:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class ClearAllFavorites(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def post(self, request, user_id):
        user = self.get_user(user_id)
        favorite_recipes = FavoriteRecipes.objects.filter(user=user)
        favorite_collections = FavoriteCollections.objects.filter(user=user)
        favorite_recipes.delete()
        favorite_collections.delete()
        return Response(status=status.HTTP_200_OK)