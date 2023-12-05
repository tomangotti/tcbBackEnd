from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from django.contrib.auth.models import User
from .models import Messages
from .serializer import MessagesSerializer

import os

from openai import OpenAI
client = OpenAI(api_key='')


# Create your views here.
class GetUsersMessages(APIView):
    def get(self, request, code):
        user = code
        messages = Messages.objects.filter(user=user).order_by('created_at')
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostNewMessage(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def post(self, request):
        user_id = request.data.get('user')
        user = self.get_user(user_id)
        serializer = MessagesSerializer(data=request.data)

        if serializer.is_valid():
            message = Messages.objects.create(user=user, content=serializer.data['content'], role='user')
            message.save()
            print(message.content)
            res = gerate_openai_response(serializer.data['content'], user)
            print(res)
            ai_message = Messages.objects.create(user=user, content=res, role='system')
            ai_message.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



def gerate_openai_response(content, user):

    messages = [
        {"role": "system", "content": "You are a helpful cooking assistant."},
        {"role": "system", "content": "You job is to help users find recipes that are in the database or to help them create new recipes."},
        {"role": "user", "content": content},
    ]
    print('we about to send this to openai')

    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)  
    
    return completion.choices[0].message.content




class MessageAPIView(APIView):
    def post(self, request):
        pass


class ClearUserMessages(APIView):

    def delete(self, request, code):
        print(code)
        user = code
        messages = Messages.objects.filter(user=user)
        messages.delete()
        return Response({"Message": "Messages deleted"},status=status.HTTP_200_OK)