from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import RandomCode
from recipes.models import Recipes
from social.models import Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

class ProfileInformationSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(user=obj).count()

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()
    
    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'recipes_count', 'followers_count', 'following_count')

class RandomCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = RandomCode
        fields = ('id', 'code', 'created_at', 'user', 'approved', 'email')


class QuickGlanceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profileimage.image', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'image')