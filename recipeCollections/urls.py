from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import GetUsersCollections, PostNewCollection, AddRecipeToCollection, RemoveRecipeFromCollection, DeleteCollection


urlpatterns = [
    path("user/get/<str:code>", GetUsersCollections.as_view()),
    path("post-new-collection/<str:code>", PostNewCollection.as_view()),
    path("add-recipe/<int:collection_id>/<int:recipe_id>", AddRecipeToCollection.as_view()),
    path("remove-recipe/<int:collection_id>/<int:recipe_id>", RemoveRecipeFromCollection.as_view()),
    path("delete/<int:collection_id>", DeleteCollection.as_view()),
]
