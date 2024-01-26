
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.db import transaction


from .serializers import UserSerializer, UserLoginSerializer, CreateUserSerializer, ProfileInformationSerializer
from rest_framework.views import APIView
from recipes.models import Recipes
from recipes.serializers import RecipesSerializer



class GetAllUsers(APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateNewUser(APIView):
   def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            if User.objects.filter(username=validated_data['username']).exists() or User.objects.filter(email=validated_data['email']).exists():
                return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User(username=validated_data['username'], email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
            user.password = make_password(validated_data['password'])
            user.save()
            print(user)

            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            return Response({'message': 'User created successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckLoggedInView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({'message': 'User is logged in', 'user_id': user.id})
    

class GetUserInfo(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EditUser(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer  # Replace with your user serializer
    queryset = User.objects.all()  # Replace with your user model queryset

    def get_object(self):
        # Retrieve the user object based on the authenticated user
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class GetUsersProfileInformation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, code, *args, **kwargs):
        user = get_object_or_404(User, id=code)
        serializer = ProfileInformationSerializer(user)
        recipes = Recipes.objects.filter(user=user)
        recipes_serializer = RecipesSerializer(recipes, many=True)

        return Response([serializer.data, recipes_serializer.data], status=status.HTTP_200_OK)