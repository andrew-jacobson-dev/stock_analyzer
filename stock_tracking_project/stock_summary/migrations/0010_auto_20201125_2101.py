# Generated by Django 3.1.3 on 2020-11-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0009_auto_20201125_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockeod',
            name='a_fifty_two_week_delta',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_low_high_delta',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
