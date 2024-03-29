# Generated by Django 4.2.4 on 2024-03-04 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipeCollections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recipeCollections.collections')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
