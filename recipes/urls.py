from django.urls import path

from .views import  GetAllRecipes, GetIngredients, GetRecipeDetails, GetUserSavedRecipes, PostASavedRecipe

urlpatterns = [
    
    path("recipe-saved", PostASavedRecipe.as_view()),
    path("all", GetAllRecipes.as_view()),
    path("<str:code>", GetRecipeDetails.as_view()),
    path("ingredients/<str:code>", GetIngredients.as_view()),
    path("saved/<str:code>", GetUserSavedRecipes.as_view())
]