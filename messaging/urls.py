from django.urls import path

from .views import GetUsersMessages, PostNewMessage, MessageAPIView


urlpatterns = [
    path("get/<str:code>", GetUsersMessages.as_view()),
    path("post-new-message", PostNewMessage.as_view()),
    path("messages", MessageAPIView.as_view()),
]
