# Generated by Django 5.0.2 on 2024-03-16 03:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0014_alter_chats_chat_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='chat_data',
            field=models.JSONField(default={'chat_data': [], 'chat_time': 1710560304}),
        ),
        migrations.AlterField(
            model_name='prescriptions',
            name='prescription_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
