from django.urls import path

from .views import EditUser ,GetUserInfo, GetAllUsers, CreateNewUser, UserLoginView, CheckLoggedInView

urlpatterns = [
    path("getUserInfo", GetUserInfo.as_view()),
    path("create", CreateNewUser.as_view()),
    path("login", UserLoginView.as_view()),
    path('check-logged-in', CheckLoggedInView.as_view()),
    path('<str:code>/update', EditUser.as_view()),
]




