# Generated by Django 3.1.3 on 2020-12-18 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0021_userstock_a_invested'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['t_short_name']},
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_beta',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_forward_eps',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_forward_pe',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_market_cap',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_payout_ratio',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockeod',
            name='a_trailing_eps',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]