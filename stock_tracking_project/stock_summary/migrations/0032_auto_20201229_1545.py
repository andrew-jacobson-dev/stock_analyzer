# Generated by Django 3.1.3 on 2020-12-29 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0031_auto_20201229_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockeodprofile',
            old_name='q_percent_change',
            new_name='q_consecutive_days_percent_change',
        ),
    ]
