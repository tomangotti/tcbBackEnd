from .models import ShoppingList, ListItems, SharedLists
from .serializers import ShoppingListSerializer, ListItemsSerializer, SharedListsSerializer, ShoppingListAndItemsSerializer
from recipes.models import Recipes, ingredients
from django.contrib.auth.models import User



def create_new_shopping_list(request, user):
    shopping_list = ShoppingList.objects.create(user=user, name=request.data['name'])
    shopping_list.save()
    serialize = ShoppingListSerializer(shopping_list)
    return serialize.data


def delete_shopping_list(list_id, user):
    shopping_list = ShoppingList.objects.get(id=list_id)
    if shopping_list.user != user:
        return False
    shopping_list.delete()

    return True



def get_users_shopping_lists(user):
    shopping_lists = ShoppingList.objects.filter(user=user)
    # shared_Lists = SharedLists.objects.filter(user=user)
    # all_lists = shopping_lists | shared_Lists
    serializer = ShoppingListSerializer(shopping_lists, many=True)

    return serializer.data



def add_item_to_shopping_list(request, shopping_list):
    item = ListItems.objects.create(shopping_list=shopping_list, quantity=request.data['quantity'], quantity_type=request.data['quantity_type'], name=request.data['name'], checked=False)
    item.save()
    
    serializer = ListItemsSerializer(item)
    return serializer.data

def remove_item_from_shopping_list(item_id):
    item = ListItems.objects.get(id=item_id)
    item.delete()

    return True

def change_item_status(item_id):
    item = ListItems.objects.get(id=item_id)
    item.checked = not item.checked
    item.save()

    return item


def add_recipe_ingredients_to_shopping_list(request, shopping_list, recipe):
    list_items = ingredients.objects.filter(recipe=recipe)
    new_items = []
    for list_item in list_items:
        item = ListItems.objects.create(shopping_list=shopping_list, recipe=recipe, quantity=list_item.quantity, quantity_type=list_item.quantity_type, name=list_item.name, checked=False)
        item.save()
        new_items.append(item)
    
    serializer = ListItemsSerializer(new_items, many=True)
    
    return serializer.data
    

def get_shopping_list_details(list_id):
    shopping_list = ShoppingList.objects.get(id=list_id)
    serializer = ShoppingListAndItemsSerializer(shopping_list)
    return serializer.data