# Generated by Django 3.1.3 on 2021-01-04 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_auto_20210104_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstocktransaction',
            name='t_notes',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
