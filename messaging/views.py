from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from django.contrib.auth.models import User
from .models import Messages
from .serializer import MessagesSerializer
from recipes.models import Recipes


import os

from openai import OpenAI
key = os.environ.get('OPENAI_API_SECRET_KEY')
# key = ""
client = OpenAI(api_key=key)


# Create your views here.
class GetUsersMessages(APIView):
    def get(self, request, code):
        user = code
        messages = Messages.objects.filter(user=user).order_by('created_at')
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# Posting new message in chat with chat bot
class PostNewMessage(APIView):
    def get_user(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def post(self, request):
        user_id = request.data.get('user')
        user = self.get_user(user_id)
        print(request.data)
        serializer = MessagesSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            message = Messages.objects.create(user=user, content=serializer.data['content'], role='user')
            print(message)
            message.save()
            res = generate_openai_response(serializer.data['content'], user)
            ai_message = Messages.objects.create(user=user, content=res, role='system')
            response_serializer = MessagesSerializer(ai_message)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# function sending message to OPENAI API 
def generate_openai_response(content, user):
    print("hello from ai response")
    recipes = Recipes.objects.all()
    recipes_list = []
    for recipe in recipes:
        ingredients_list = recipe.ingredients.values_list('name', 'quantity', 'quantity_type')

        recipe_info = {
            "name": recipe.name,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "published": recipe.published,
            "category": recipe.category,
            "servings": recipe.servings,
            "cook_time": recipe.cook_time,
            "ingredients": [{"name": name, "quantity": quantity, "quantity_type": quantity_type} for name, quantity, quantity_type in ingredients_list],
        }
        recipes_list.append(recipe_info)

    message_list = Messages.objects.filter(user=user).order_by('created_at')

    messages = [
        {"role": "system", "content": "You are a helpful cooking assistant."},
        {"role": "system", "content": "You job is to help users find recipes that are in the database or to help them create new recipes. Please prioritize finding recipes that are already in the database."},
        {"role": "system", "content": f"Here is the recipe database:{recipes_list}"},
        {"role": "system", "content": "Here is the conversation so far:"},
    ]

    for message in message_list:
        if message.role == 'user':
            messages.append({"role": "user", "content": message.content})
        else:
            messages.append({"role": "system", "content": message.content})

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
    