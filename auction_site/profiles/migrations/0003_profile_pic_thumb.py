# Generated by Django 5.2.4 on 2025-07-11 18:20

import profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_pic_original_alter_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pic_thumb',
            field=models.ImageField(blank=True, null=True, upload_to=profiles.models.profile_thumb_upload_to),
        ),
    ]
