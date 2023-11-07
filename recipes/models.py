from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    instructions = models.CharField(max_length=1000)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=4)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)

    def __str__ (self):
        return self.name
    
    def resize_image(self):
        # Open the uploaded image using Pillow
        img = Image.open(self.image.path)

        # Set a maximum width and height for the resized image
        max_width = 800  # Adjust this to your desired maximum width
        max_height = 800  # Adjust this to your desired maximum height

        # Check if the image dimensions exceed the maximum size
        if img.width > max_width or img.height > max_height:
            # Resize the image while preserving its aspect ratio
            img.thumbnail((max_width, max_height))

            # Save the resized image back to the same path
            img.save(self.image.path)

    def save(self, *args, **kwargs):
        # Resize the image before saving
        self.resize_image()
        super().save(*args, **kwargs)
    

class ingredients(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50, default="")
    quantity_type = models.CharField(max_length=50, default="")
    recipe = models.ForeignKey(Recipes, related_name='ingredients', on_delete=models.CASCADE)

    def __str__ (self):
        return self.name
    


class SavedRecipes(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cart(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
