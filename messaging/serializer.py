from rest_framework import serializers
from .models import Messages



class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('id', 'user', 'content', 'role', 'created_at')
        extra_kwargs = {'user': {'required': False}}