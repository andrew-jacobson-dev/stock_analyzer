# Generated by Django 3.1.3 on 2020-11-26 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0010_auto_20201125_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockeod',
            name='a_previous_close_change',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
