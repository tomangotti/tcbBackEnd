from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from recipes.models import Recipes
from django.contrib.auth.models import User
from .models import Collections, CollectionRating
from .serializer import CollectionSerializer, CollectionRatingSerializer
from ususers.serializers import UserSerializer
from recipes.serializers import RecipesSerializer


class GetAllPublishedCollections(APIView):
    def get(self, request):
        collections = Collections.objects.filter(published=True).order_by('created_at')
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            collection = Collections.objects.create(user=user, name=serializer.data['name'], description=serializer.data['description'], published=serializer.data.get('published', False))
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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get_recipe(self, recipe_id):
        return get_object_or_404(Recipes, pk=recipe_id)

    def post(self, request, collection_id, recipe_id):
        user = request.user
        
        collection = self.get_collection(collection_id)
        recipe = self.get_recipe(recipe_id)

        if collection.user != user:
            return Response({'message': 'You are not authorized to remove this recipe'}, status=status.HTTP_403_FORBIDDEN)
        
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
    permission_classes = [permissions.IsAuthenticated]

    def get_collection(self, collection_id, user_id):
        return get_object_or_404(Collections, pk=collection_id, user=user_id)
    
    def delete(self, request, collection_id):
        print(collection_id)
        print(request.user)
        
        user = request.user
        user_serializer = UserSerializer(user)
        
        collection = self.get_collection(collection_id, user_serializer.data['id'])
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
    permission_classes = [permissions.IsAuthenticated]

    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def patch(self, request, collection_id):
        collection = self.get_collection(collection_id)
        print(request.data)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class GetUsersCollectionRating(APIView):
    seriaizer_class = CollectionRatingSerializer

    def get(self, request, user_id, collection_id, format=None):

        if CollectionRating.objects.filter(user=user_id, collection=collection_id).exists():
            rating = CollectionRating.objects.get(user=user_id, collection=collection_id)
            serializer = CollectionRatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No rating found'},status=status.HTTP_200_OK)
        



class AddNewRatingView(APIView):
    serializer_class = CollectionRatingSerializer

    def post(self, request):
        serializer = CollectionRatingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            collection_id = validated_data['collection']
            user_id = validated_data['user']
            rating = validated_data['rating']

            print(collection_id)
            print(user_id)
            print(rating)

            if CollectionRating.objects.filter(user=user_id, collection=collection_id):
                old_rating = CollectionRating.objects.get(user=user_id, collection=collection_id)
                old_rating.delete()

            rating = CollectionRating(user=user_id, collection=collection_id, rating=rating)
            rating.save()
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_200_OK)
            
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class GetCollectionToBeEdited(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_collection(self, collection_id):
        return get_object_or_404(Collections, pk=collection_id)

    def get(self, request, collection_id):
        user = request.user
        collection = self.get_collection(collection_id)
        serializer = CollectionSerializer(collection)

        users_recipes = Recipes.objects.filter(user=user, published = True)
        recipes_serializer = RecipesSerializer(users_recipes, many=True)
        recipe_data = recipes_serializer.data

        return Response(serializer.data, status=status.HTTP_200_OK)