# Generated by Django 3.1.3 on 2020-12-17 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0020_auto_20201217_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstock',
            name='a_invested',
            field=models.DecimalField(decimal_places=3, max_digits=8, null=True),
        ),
    ]
