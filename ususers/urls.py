from django.urls import path

from .views import  CreateRandomCode, ApproveRandomCode, ChangeUserPassword, SendSampleEmail, EditUser ,GetUserInfo, GetAllUsers, CreateNewUser, UserLoginView, CheckLoggedInView, GetUsersProfileInformation

urlpatterns = [
    path("getUserInfo", GetUserInfo.as_view()),
    path("create", CreateNewUser.as_view()),
    path("login", UserLoginView.as_view()),
    path('check-logged-in', CheckLoggedInView.as_view()),
    path('<str:code>/update', EditUser.as_view()),
    path('profile/<str:code>', GetUsersProfileInformation.as_view()),
    path('all', GetAllUsers.as_view()),
    path('send/code', CreateRandomCode.as_view()),
    path('approve/code', ApproveRandomCode.as_view()),
    path('change/password', ChangeUserPassword.as_view()),
]





