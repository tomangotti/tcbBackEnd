from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
        extra_kwargs = {'follower': {'required': False}, 'following': {'required': False}}