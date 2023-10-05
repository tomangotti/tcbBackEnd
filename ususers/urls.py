from django.urls import path

from .views import GetAllUsers, CreateNewUser

urlpatterns = [
    path("all", GetAllUsers.as_view()),
    path("create", CreateNewUser.as_view()),
]

