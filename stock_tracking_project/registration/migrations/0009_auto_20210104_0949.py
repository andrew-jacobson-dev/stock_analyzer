# Generated by Django 3.1.3 on 2021-01-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20210104_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstocktransaction',
            name='t_notes',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
