# Generated by Django 3.1.6 on 2021-03-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_auto_20210311_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grammuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
    ]
