# Generated by Django 3.0.8 on 2022-08-13 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20220812_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api7',
            name='today_sunrise',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='api7',
            name='today_sunset',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='api7',
            name='tomorrow_sunrise',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='api7',
            name='tomorrow_sunset',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
    ]
