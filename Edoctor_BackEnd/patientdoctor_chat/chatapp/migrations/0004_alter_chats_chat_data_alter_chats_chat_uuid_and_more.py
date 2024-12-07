# Generated by Django 5.0.2 on 2024-03-15 02:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_patientrecords_record_uuid_alter_chats_chat_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='chat_data',
            field=models.JSONField(default={'chat_data': [], 'chat_time': 1710470786}),
        ),
        migrations.AlterField(
            model_name='chats',
            name='chat_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='patientrecords',
            name='record_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
