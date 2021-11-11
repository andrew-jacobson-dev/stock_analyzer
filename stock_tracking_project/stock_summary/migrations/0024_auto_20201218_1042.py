# Generated by Django 3.1.3 on 2020-12-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0023_auto_20201218_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockeod',
            name='a_beta',
            field=models.DecimalField(decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='stockeod',
            name='a_forward_eps',
            field=models.DecimalField(decimal_places=3, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='stockeod',
            name='a_forward_pe',
            field=models.DecimalField(decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockeod',
            name='a_market_cap',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='stockeod',
            name='a_trailing_eps',
            field=models.DecimalField(decimal_places=3, max_digits=8, null=True),
        ),
    ]
