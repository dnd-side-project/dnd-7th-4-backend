# Generated by Django 3.0.8 on 2022-08-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_delete_user_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api6',
            name='pm10Grade1h',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='api6',
            name='pm10Value24',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='api6',
            name='pm25Grade1h',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='api6',
            name='pm25Value24',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
    ]
