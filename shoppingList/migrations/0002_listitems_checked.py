# Generated by Django 3.2.23 on 2024-06-18 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitems',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
