from .serializers import RecipesSerializer
from recipeCollections.serializer import CollectionSerializer
from ususers.serializers import QuickGlanceSerializer
from ususers.models import User, ProfileImage



def transform_recipe_data(recipe_list, request):
    serializer = RecipesSerializer(recipe_list, many=True)
    serializer_data = serializer.data

    for recipe_data in serializer_data:
        if recipe_data['image']:
            recipe_data['image'] = request.build_absolute_uri(recipe_data['image'])

    return serializer_data



def transform_collection_data(collection):
    serializer = CollectionSerializer(collection, many=True)
    serializer_data = serializer.data

    return serializer_data


def transform_user_data(user, request):
    serializer = QuickGlanceSerializer(user, many=True)
    serializer_data = serializer.data

    for user_data in serializer_data:
        if user_data['profile_image']:
            user_data['profile_image'] = request.build_absolute_uri(user_data['profile_image'])

    return serializer_data