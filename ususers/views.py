from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import User
from .serializers import UserSerializer



class GetAllUsers(APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        print(users)
        serializer = UserSerializer(users, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateNewUser(generics.CreateAPIView):
    serializer_class = UserSerializer
