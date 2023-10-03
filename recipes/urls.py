from django.urls import path

from .views import  GetAllRecipes, GetIngredients, GetRecipeDetails

urlpatterns = [
    path("all", GetAllRecipes.as_view()),
    path("<str:code>", GetRecipeDetails.as_view()),
    path("ingredients/<str:code>", GetIngredients.as_view())
]