# Generated by Django 3.1.6 on 2021-03-17 01:52

import basic.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0007_auto_20210316_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=stdimage.models.StdImageField(upload_to=basic.models.Photo.user_directory_path),
        ),
    ]