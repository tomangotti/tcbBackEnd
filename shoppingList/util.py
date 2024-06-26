from .models import ShoppingList, ListItems, SharedLists
from .serializers import ShoppingListSerializer, ListItemsSerializer, SharedListsSerializer, ShoppingListAndItemsSerializer
from recipes.models import Recipes, ingredients
from django.contrib.auth.models import User



def create_new_shopping_list(request, user):
    shopping_list = ShoppingList.objects.create(user=user, name=request.data['name'])
    shopping_list.save()
    serialize = ShoppingListSerializer(shopping_list)
    return serialize.data



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
    ingredients = recipe.ingredients.all()
    for ingredient in ingredients:
        item = ListItems.objects.create(shopping_list=shopping_list, recipe=recipe, quantity=ingredient.quantity, quantity_type=ingredient.quantity_type, name=ingredient.name, checked=False)
        item.save()
    
    return item

def get_shopping_list_details(list_id):
    shopping_list = ShoppingList.objects.get(id=list_id)
    serializer = ShoppingListAndItemsSerializer(shopping_list)
    return serializer.data