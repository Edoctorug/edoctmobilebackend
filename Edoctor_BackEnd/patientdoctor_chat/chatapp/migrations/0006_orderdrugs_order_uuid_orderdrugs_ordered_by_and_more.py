# Generated by Django 5.0.2 on 2024-03-16 02:33

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_appointments_appointment_details_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdrugs',
            name='order_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='orderdrugs',
            name='ordered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_by', to='chatapp.hospitalusers'),
        ),
        migrations.AlterField(
            model_name='chats',
            name='chat_data',
            field=models.JSONField(default={'chat_data': [], 'chat_time': 1710556389}),
        ),
        migrations.AlterField(
            model_name='orderdrugs',
            name='assigned_pharmacy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_pharma', to='chatapp.hospitalusers'),
        ),
        migrations.AlterField(
            model_name='orderdrugs',
            name='delivery_man',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_man', to='chatapp.hospitalusers'),
        ),
        migrations.AlterField(
            model_name='orderdrugs',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='chatapp.hospitalusers'),
        ),
    ]
