from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import FollowingView, FollowersView, FollowUserView, UnfollowUserView

urlpatterns = [
    path("following", FollowingView.as_view()),
    path("followers", FollowersView.as_view()),
    path("follow/<str:code>", FollowUserView.as_view()),
    path("unfollow/<str:code>", UnfollowUserView.as_view()),
]