# Generated by Django 3.1.3 on 2020-11-30 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockalert',
            name='d_closed',
            field=models.DateField(default='9999-12-31', null=True),
        ),
    ]
