from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import shoppingList.views as views
from .views import *

url_patterns = [
    path('create/new/shopping_list', CreateNewShoppingList.as_view()),
    path('get/users/shopping_lists', GetUsersShoppingLists.as_view()),
    path('add/item/to/shopping_list/<int:list_id>', AddNewItemToShoppingList.as_view()),
    path('add/recipe_ingredients/shopping_list/<int:list_id>/<int:recipe_id>', AddRecipeIngredientsToShopingList.as_view()),
]
