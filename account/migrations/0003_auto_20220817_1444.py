# Generated by Django 3.0.8 on 2022-08-17 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220816_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.TextField(default='', null=True),
        ),
    ]