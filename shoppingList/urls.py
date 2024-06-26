from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import shoppingList.views as views
from .views import DeleteShoppingList, GetShoppingListDetails, DeleteShoppingListItem, ChangeItemStatus, CreateNewShoppingList, GetUsersShoppingLists, AddNewItemToShoppingList, AddRecipeIngredientsToShopingList

urlpatterns = [
    path('create/new/shopping_list', CreateNewShoppingList.as_view()),
    path('get/users/<int:user_id>', GetUsersShoppingLists.as_view()),
    path('add/item/to/shopping_list/<int:list_id>', AddNewItemToShoppingList.as_view()),
    path('add/recipe_ingredients/shopping_list/<int:list_id>/<int:recipe_id>', AddRecipeIngredientsToShopingList.as_view()),
    path('delete/item/<int:item_id>', DeleteShoppingListItem.as_view()),
    path('change/item/status/<int:item_id>', ChangeItemStatus.as_view()),
    path('get/details/<int:list_id>', GetShoppingListDetails.as_view()),
    path('delete/shopping_list/<int:list_id>', DeleteShoppingList.as_view())

]
