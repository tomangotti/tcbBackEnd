# Generated by Django 4.2.4 on 2024-01-15 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_recipes_category_recipes_cook_time_recipes_servings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='category',
            field=models.CharField(default='other', max_length=50),
        ),
    ]
