# Generated by Django 3.0.8 on 2022-08-09 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220808_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Api_6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sidoName', models.CharField(max_length=2)),
                ('stationName', models.CharField(max_length=10)),
                ('pm10Grade1h', models.IntegerField()),
                ('pm25Grade1h', models.IntegerField()),
                ('pm10Value24', models.IntegerField()),
                ('pm25Value24', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='region',
            name='api6_station',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='region',
            name='api6_id',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Api_6'),
        ),
    ]
