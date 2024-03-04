from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import AddNewRatingView, GetUsersCollectionRating, UpdateCollection ,GetUsersCollections, PostNewCollection, AddRecipeToCollection, RemoveRecipeFromCollection, DeleteCollection, GetSingleCollection


urlpatterns = [
    path("user/get/<str:code>", GetUsersCollections.as_view()),
    path("post-new-collection/<str:code>", PostNewCollection.as_view()),
    path("add-recipe/<int:collection_id>/<int:recipe_id>", AddRecipeToCollection.as_view()),
    path("remove-recipe/<int:collection_id>/<int:recipe_id>", RemoveRecipeFromCollection.as_view()),
    path("delete/<int:collection_id>", DeleteCollection.as_view()),
    path("get-single/<int:collection_id>", GetSingleCollection.as_view()),
    path("update/<int:collection_id>", UpdateCollection.as_view()),
    path("<str:collection_id>/ratings/<str:user_id>", GetUsersCollectionRating.as_view()),
    path("ratings/new", AddNewRatingView.as_view()),
]


