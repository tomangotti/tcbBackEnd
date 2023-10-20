from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
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
    
