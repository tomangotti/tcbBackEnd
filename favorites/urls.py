from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import GetSpecificFavoriteCollectionCheck, ClearAllFavorites, AddRecipeToFavorites, RemoveRecipeFromFavorites, AddCollectionToFavorites, RemoveCollectionFromFavorites, GetUsersFavoriteRecipes, GetUsersFavoriteCollections, GetSpecificFavoriteRecipeCheck

urlpatterns = [
    path('recipes/user/get/<str:user_id>', GetUsersFavoriteRecipes.as_view()),
    path('collections/user/get/<str:user_id>', GetUsersFavoriteCollections.as_view()),
    path('recipes/add/<str:user_id>/<int:recipe_id>', AddRecipeToFavorites.as_view()),
    path('recipes/remove/<str:user_id>/<int:recipe_id>', RemoveRecipeFromFavorites.as_view()),
    path('collections/add/<str:user_id>/<int:collection_id>', AddCollectionToFavorites.as_view()),
    path('collections/remove/<str:user_id>/<int:collection_id>', RemoveCollectionFromFavorites.as_view()),
    path('recipes/check/<str:user_id>/<int:recipe_id>', GetSpecificFavoriteRecipeCheck.as_view()),
    path('collections/check/<str:user_id>/<int:collection_id>', GetSpecificFavoriteCollectionCheck.as_view()),
    path('clear/<str:user_id>', ClearAllFavorites.as_view()),
]
