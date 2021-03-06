# Generated by Django 3.1.3 on 2021-01-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0033_auto_20201230_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockeodprofile',
            name='a_consecutive_days_volume_change',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeodprofile',
            name='q_consecutive_days_volume_growth',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeodprofile',
            name='q_consecutive_days_volume_percent_change',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
