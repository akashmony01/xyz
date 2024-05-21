# Generated by Django 5.0.6 on 2024-05-21 04:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_doctor_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]