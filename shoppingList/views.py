from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import ShoppingList, ListItems, SharedLists
from .serializers import ShoppingListSerializer, ListItemsSerializer, SharedListsSerializer, ShoppingListAndItemsSerializer
from recipes.models import Recipes
from django.contrib.auth.models import User
from .util import *

# Create your views here.



class GetUsersShoppingLists(APIView):

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)
        shopping_lists = get_users_shopping_lists(user)

        return Response(shopping_lists, status=status.HTTP_200_OK)



class CreateNewShoppingList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        shopping_list = create_new_shopping_list(request, user)

        return Response(shopping_list, status=status.HTTP_201_CREATED)
    



class AddNewItemToShoppingList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, list_id, format=None):
        
        shopping_list = get_object_or_404(ShoppingList, id=list_id)
        item = add_item_to_shopping_list(request, shopping_list)

        return Response(item, status=status.HTTP_201_CREATED)
    


class AddRecipeIngredientsToShopingList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, list_id, recipe_id, format=None):
        user = request.user
        shopping_list = get_object_or_404(ShoppingList, id=list_id)
        recipe = get_object_or_404(Recipes, id=recipe_id)
        item = add_recipe_ingredients_to_shopping_list(request, shopping_list, recipe)

        return Response(item, status=status.HTTP_201_CREATED)



class GetShoppingListDetails(APIView):

    def get(self, request, list_id, format=None):

        detail = get_shopping_list_details(list_id)

        return Response(detail, status=status.HTTP_200_OK)
    

class DeleteShoppingListItem(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id, format=None):
        remove_item_from_shopping_list(item_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ChangeItemStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, item_id, format=None):
        item = change_item_status(item_id)

        return Response(item, status=status.HTTP_200_OK)

