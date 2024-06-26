

from rest_framework import serializers
from .models import ShoppingList, ListItems, SharedLists

class ShoppingListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    items = serializers.StringRelatedField(many=True)
    shared_list = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = ShoppingList
        fields = ('id', 'name', 'user_username', 'user', 'items', 'shared_list')

class ListItemsSerializer(serializers.ModelSerializer):
    shopping_list_name = serializers.CharField(source='shopping_list.name', read_only=True)
    
    class Meta:
        model = ListItems
        fields = ('id', 'shopping_list', 'shopping_list_name', 'recipe', 'quantity', 'quantity_type', 'name', 'checked')

class SharedListsSerializer(serializers.ModelSerializer):
    shopping_list_name = serializers.CharField(source='shopping_list.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = SharedLists
        fields = ('id', 'shopping_list', 'shopping_list_name', 'user', 'user_username')


class ShoppingListAndItemsSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    items = ListItemsSerializer(many=True, read_only=True)
    
    class Meta:
        model = ShoppingList
        fields = ('id', 'name', 'user_username', 'user', 'items')