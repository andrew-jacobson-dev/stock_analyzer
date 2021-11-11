# Generated by Django 3.1.3 on 2020-12-29 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20201228_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstock',
            name='a_invested',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='userstock',
            name='a_share_price_bought',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='userstock',
            name='q_shares_owned',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9, null=True),
        ),
    ]
