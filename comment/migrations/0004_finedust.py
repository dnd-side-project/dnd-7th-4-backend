# Generated by Django 3.0.8 on 2022-08-15 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20220815_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finedust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('imageUrl', models.TextField(max_length=100)),
                ('standard', models.IntegerField(choices=[('1', '좋음, 보통'), ('2', '나쁨'), ('3', '매우 나쁨')], max_length=50)),
            ],
        ),
    ]