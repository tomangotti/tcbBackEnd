from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import  GetAllRecipes, GetIngredients, GetRecipeDetails, GetUserSavedRecipes, PostASavedRecipe, PostNewRecipe

urlpatterns = [
    path("recipe-saved", PostASavedRecipe.as_view()),
    path("addNew", PostNewRecipe.as_view()),
    path("all", GetAllRecipes.as_view()),
    path("<str:code>", GetRecipeDetails.as_view()),
    path("ingredients/<str:code>", GetIngredients.as_view()),
    path("saved/<str:code>", GetUserSavedRecipes.as_view()),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)