from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from recipes.models import Recipes
from django.contrib.auth.models import User
from .models import Collections
from .serializer import CollectionSerializer


# class Collections(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField(max_length=5000)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
#     recipes = models.ManyToManyField(Recipes,related_name='collections', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    

#     def __str__ (self):
#         return self.name

class GetUsersCollections(APIView):
    def get(self, request, code):
        user = code
        collections = Collections.objects.filter(user=user).order_by('created_at')
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostNewCollection(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def post(self, request, code):
        user_id = code
        user = self.get_user(user_id)
        print(request.data)
        serializer = CollectionSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            collection = Collections.objects.create(user=user, name=serializer.data['name'], description=serializer.data['description'])
            collection.recipes.set(serializer.data.get('recipes', []))
            print(collection)
            collection.save()
            # for recipe_id in serializer.data.get('recipes', []):
            #     recipe = get_object_or_404(Recipes, pk=recipe_id)
            #     collection.recipes.add(recipe)
                
            # collection.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddRecipeToCollection(APIView):
    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get_recipe(self, recipe_id):
        return get_object_or_404(Recipes, pk=recipe_id)

    def post(self, request, collection_id, recipe_id):
        collection = self.get_collection(collection_id)
        recipe = self.get_recipe(recipe_id)
        collection.recipes.add(recipe)
        return Response(status=status.HTTP_200_OK)
    
class RemoveRecipeFromCollection(APIView):
    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get_recipe(self, recipe_id):
        return get_object_or_404(Recipes, pk=recipe_id)

    def post(self, request, collection_id, recipe_id):
        collection = self.get_collection(collection_id)
        recipe = self.get_recipe(recipe_id)
        collection.recipes.remove(recipe)
        return Response(status=status.HTTP_200_OK)
    
class GetCollectionDetails(APIView):
    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get(self, request, collection_id):
        collection = self.get_collection(collection_id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DeleteCollection(APIView):
    def get_collection(self, collection_id, user_id):
        return get_object_or_404(Collections, pk=collection_id, user=user_id)
    
    def delete(self, request, collection_id):
        user = request.user
        collection = self.get_collection(collection_id, user.id)
        collection.delete()
        return Response(status=status.HTTP_200_OK)
    

class GetSingleCollection(APIView):
    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get(self, request, collection_id):
        collection = self.get_collection(collection_id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateCollection(APIView):
    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def put(self, request, collection_id):
        collection = self.get_collection(collection_id)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)