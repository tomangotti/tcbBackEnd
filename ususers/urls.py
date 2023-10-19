from django.urls import path

from .views import GetUserInfo, GetAllUsers, CreateNewUser, UserLoginView, CheckLoggedInView

urlpatterns = [
    path("getUserInfo", GetUserInfo.as_view()),
    path("create", CreateNewUser.as_view()),
    path("login", UserLoginView.as_view()),
    path('check-logged-in', CheckLoggedInView.as_view())
]




