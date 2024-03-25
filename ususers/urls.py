from django.urls import path

from .views import  SendSampleEmail, EditUser ,GetUserInfo, GetAllUsers, CreateNewUser, UserLoginView, CheckLoggedInView, GetUsersProfileInformation

urlpatterns = [
    path("getUserInfo", GetUserInfo.as_view()),
    path("create", CreateNewUser.as_view()),
    path("login", UserLoginView.as_view()),
    path('check-logged-in', CheckLoggedInView.as_view()),
    path('<str:code>/update', EditUser.as_view()),
    path('profile/<str:code>', GetUsersProfileInformation.as_view()),
    path('all', GetAllUsers.as_view()),
    path('send', SendSampleEmail.as_view())
    
]





