# Generated by Django 3.1.3 on 2020-11-25 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0003_auto_20201125_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockowned',
            name='id',
        ),
        migrations.RemoveField(
            model_name='stockwatch',
            name='id',
        ),
        migrations.AlterField(
            model_name='stockowned',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock_summary.stock'),
        ),
        migrations.AlterField(
            model_name='stockwatch',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock_summary.stock'),
        ),
    ]
