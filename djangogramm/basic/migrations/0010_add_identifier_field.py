# Generated by Django 3.1.6 on 2021-03-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0009_auto_20210318_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
        migrations.AddField(
            model_name='profile',
            name='identifier',
            field=models.CharField(db_index=True, max_length=128, null=True),
        ),
    ]
