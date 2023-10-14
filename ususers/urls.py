from django.urls import path

from .views import GetAllUsers, CreateNewUser, UserLoginView, CheckLoggedInView

urlpatterns = [
    path("information/<str:id>", GetAllUsers.as_view()),
    path("create", CreateNewUser.as_view()),
    path("login", UserLoginView.as_view()),
    path('check-logged-in', CheckLoggedInView.as_view())
]


