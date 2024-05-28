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
            user_id = user_data['id']
            try:
                user = User.objects.get(pk=user_id)
                if ProfileImage.objects.filter(user=user):
                    profile_image = ProfileImage.objects.get(user=user)
                    if profile_image.image:
                        image_url = request.build_absolute_uri(profile_image.image.url)
                        user_data['image'] = image_url
            except User.DoesNotExist:
                pass
    return serializer_data