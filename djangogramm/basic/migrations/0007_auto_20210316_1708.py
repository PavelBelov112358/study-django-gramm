# Generated by Django 3.1.6 on 2021-03-16 17:08

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_auto_20210316_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=models.CharField(max_length=64, verbose_name='Post title'), unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Post title'),
        ),
    ]
