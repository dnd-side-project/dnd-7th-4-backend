# Generated by Django 3.0.8 on 2022-08-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20220825_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.TextField(default='https://weathercomment.s3.ap-northeast-2.amazonaws.com/대표이미지/1.png', null=True),
        ),
    ]
