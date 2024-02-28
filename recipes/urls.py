from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import   GetFeedRecipes, GetUsersRecipes, AddNewRatingView, DeleteRecipe, EditRecipe, ShareRecipeWithUser, RemoveRecipeFromCartView, GetUserCartView, DeleteRecipeView, GetAllRecipes, GetIngredients, GetRecipeDetails, GetUserSavedRecipes, AddOrRemoveSavedRecipeList, PostNewRecipe, AddRecipeToCartView, GetUsersRecipeRating 

urlpatterns = [
    path("recipe-saved", PostNewRecipe.as_view()),
    path("addNew",  AddOrRemoveSavedRecipeList.as_view()),
    path("all", GetAllRecipes.as_view()),
    path("<str:code>", GetRecipeDetails.as_view()),
    path("ingredients/<str:code>", GetIngredients.as_view()),
    path("saved/<str:code>", GetUserSavedRecipes.as_view()),
    path("delete", DeleteRecipeView.as_view()),
    path("cart/userItems/<str:code>", GetUserCartView.as_view()),
    path("cart/add", AddRecipeToCartView.as_view()),
    path("cart/remove", RemoveRecipeFromCartView.as_view()),
    path("share/recipe/<str:code>", ShareRecipeWithUser.as_view()),
    path("edit/<str:code>", EditRecipe.as_view()),
    path("delete/<str:code>", DeleteRecipe.as_view()),
    path('ratings/new', AddNewRatingView.as_view()),
    path('users/<str:code>', GetUsersRecipes.as_view()),
    path('<str:recipe_id>/ratings/<str:user_id>',GetUsersRecipeRating.as_view()),
    path('feed/recipes', GetFeedRecipes.as_view()),
]



