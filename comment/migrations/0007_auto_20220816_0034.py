# Generated by Django 3.0.8 on 2022-08-16 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_windchill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windchill',
            name='standard',
            field=models.CharField(choices=[('0', '이상 없음'), ('1', '여름철 관심'), ('2', '여름철 주의'), ('3', '여름철 경고'), ('4', '여름철 위험'), ('5', '겨울철 낮음'), ('6', '겨울철 보통'), ('7', '겨울철 추움'), ('8', '겨울철 주의'), ('9', '겨울철 위험')], max_length=50),
        ),
    ]
