# Generated by Django 3.1.6 on 2021-03-19 10:24

import basic.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0012_set_identifier_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=basic.models.Profile.user_directory_path),
        ),
    ]
