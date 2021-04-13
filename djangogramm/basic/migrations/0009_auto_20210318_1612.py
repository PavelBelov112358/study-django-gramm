# Generated by Django 3.1.6 on 2021-03-18 16:12

import autoslug.fields
import basic.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_auto_20210317_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=basic.models.Post.get_slug, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='', max_length=1023, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=64),
        ),
    ]
