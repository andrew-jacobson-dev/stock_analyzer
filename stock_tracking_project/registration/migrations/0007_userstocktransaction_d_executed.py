# Generated by Django 3.1.3 on 2021-01-03 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20210103_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstocktransaction',
            name='d_executed',
            field=models.DateField(null=True),
        ),
    ]
