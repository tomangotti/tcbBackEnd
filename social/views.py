from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .models import Follow
from .serializer import FollowSerializer
from rest_framework import status


class FollowingView(APIView):
    def get(self, request):
        user = request.user
        following = Follow.objects.filter(follower=user)
        following_users = [follow.following for follow in following]
        serializer = FollowSerializer(following_users, many=True)
        return Response(serializer.data)



class FollowersView(APIView):
    def get(self, request):
        user = request.user
        followers = Follow.objects.filter(following=user)
        followers_users = [follow.follower for follow in followers]
        serializer = FollowSerializer(followers_users, many=True)
        return Response(serializer.data)



class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, code):
        user = request.user
        try:
            user_to_follow = User.objects.get(id=code)
            follow, created = Follow.objects.get_or_create(follower=user, following=user_to_follow)
            if created:
                serializer = FollowSerializer(user_to_follow)
                return Response({'message': f'You are now following user', 'user': serializer.data})
            else:
                return Response({'message': f'You are already following user'})
        except User.DoesNotExist:
            return Response({'message': f'User does not exist'}, status=status.HTTP_404_NOT_FOUND)



class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, code):
        user = request.user
        try:
            user_to_unfollow = User.objects.get(id=code)
            follow = Follow.objects.filter(follower=user, following=user_to_unfollow)
            if follow.exists():
                follow.delete()
                return Response({'message': f'You have unfollowed user'})
            else:
                return Response({'message': f'You are not following user'})
        except User.DoesNotExist:
            return Response({'message': f'User does not exist'}, status=status.HTTP_404_NOT_FOUND)



class FollowingCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, following_user_id):
        try:
            user = request.user
            following_user = User.objects.get(id=following_user_id)
            is_following = Follow.objects.filter(follower=user, following=following_user).exists()
            return Response({'is_following': is_following})
        except User.DoesNotExist:
            return Response({'message': f'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
