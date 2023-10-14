from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import  DeleteRecipeView, GetAllRecipes, GetIngredients, GetRecipeDetails, GetUserSavedRecipes, AddOrRemoveSavedRecipeList, PostNewRecipe

urlpatterns = [
    path("recipe-saved", PostNewRecipe.as_view()),
    path("addNew",  AddOrRemoveSavedRecipeList.as_view()),
    path("all", GetAllRecipes.as_view()),
    path("<str:code>", GetRecipeDetails.as_view()),
    path("ingredients/<str:code>", GetIngredients.as_view()),
    path("saved/<str:code>", GetUserSavedRecipes.as_view()),
    path("delete", DeleteRecipeView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)