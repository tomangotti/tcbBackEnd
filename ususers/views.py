
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.db import transaction

import random
import string

import os
import smtplib
import mailtrap as mt



from .serializers import  RandomCodeSerializer, UserSerializer, UserLoginSerializer, CreateUserSerializer, ProfileInformationSerializer
from rest_framework.views import APIView
from recipes.models import Recipes
from recipes.serializers import RecipesSerializer
from recipeCollections.models import Collections
from recipeCollections.serializer import CollectionSerializer
from .models import RandomCode



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
        recipes = Recipes.objects.filter(user=user).filter(published=True)
        recipes_serializer = RecipesSerializer(recipes, many=True)
        collections = Collections.objects.filter(user=user).filter(published=True)
        collections_serializer = CollectionSerializer(collections, many=True)

        return Response([serializer.data, recipes_serializer.data, collections_serializer.data], status=status.HTTP_200_OK)
    

# class RandomCode(models.Model):
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     approved = models.BooleanField(default=False)
    

class CreateRandomCode(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def generate_random_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_email(self, email, code):
        pass


    def post(self, request, *args, **kwargs):
        user_email = request.get('email')
        user = User.objects.get(email=user_email)
        
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        random_code = self.generate_random_code()
        code = RandomCode.objects.create(user=user, code=random_code, approved=False)
        code.save()
        email = self.send_email(user_email, random_code)
        if code is None:
            return Response({'error': 'Error creating code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'Code created successfully'}, status=status.HTTP_201_CREATED)
    

class ApproveRandomCode(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        code = request.get('code')
        code_obj = RandomCode.objects.get(code=code)

        if code_obj is None:
            return Response({'error': 'Code not found'}, status=status.HTTP_404_NOT_FOUND)
        
        code_obj.approved = True
        code_obj.save()
        return Response({'message': 'Code approved successfully'}, status=status.HTTP_200_OK)
    

class ChangeUserPassword(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.get('password')
        user.password = make_password(password)
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    



class SendSampleEmail(APIView):
    def get(self, request, *args, **kwargs):
        mail = mt.Mail(
            sender=mt.Address(email="mailtrap@example.com", name="Mailtrap Test"),
            to=[mt.Address(email="tom.angotti11@gmail.com")],
            subject="You are awesome!",
            text="Congrats for sending test email with Mailtrap!",
        )
        api_token = os.environ.get('MAILTRAP_API_TOKEN')
        client = mt.MailtrapClient(token=api_token)
        client.send(mail)