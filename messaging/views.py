from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import Messages
from .serializer import MessagesSerializer

# Create your views here.
class GetUsersMessages(APIView):
    def get(self, request, code):
        user = code
        messages = Messages.objects.filter(user=user).order_by('-created_at')
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class PostNewMessage(APIView):
    def post(self, request):
        print(request.data['user'])
        user_id = request.data.get('user')
        print(user_id)
        user = get_object_or_404(User, pk=user_id)
        print(user)
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)