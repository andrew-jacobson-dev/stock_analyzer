# Generated by Django 3.1.3 on 2020-12-29 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0029_auto_20201229_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockeodprofile',
            options={'ordering': ['-d_evaluation', 'stockeod__stock__n_symbol']},
        ),
        migrations.AddField(
            model_name='stockeodprofile',
            name='a_consecutive_days_price_change',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='stockeodprofile',
            unique_together={('stockeod', 'd_evaluation')},
        ),
    ]