# Generated by Django 3.1.3 on 2021-01-13 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0035_stockrecommendation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockrecommendation',
            name='d_recommendation',
        ),
        migrations.AddField(
            model_name='stockrecommendation',
            name='s_recommendation',
            field=models.DateTimeField(default='2020-01-01 10:00:00'),
            preserve_default=False,
        ),
    ]
