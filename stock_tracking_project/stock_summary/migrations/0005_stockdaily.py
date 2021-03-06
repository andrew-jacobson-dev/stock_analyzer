# Generated by Django 3.1.3 on 2020-11-25 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_summary', '0004_auto_20201125_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_process', models.DateField()),
                ('s_inserted', models.DateTimeField(auto_now_add=True)),
                ('s_updated', models.DateTimeField(auto_now=True)),
                ('a_previous_close', models.DecimalField(decimal_places=3, max_digits=8)),
                ('a_open', models.DecimalField(decimal_places=3, max_digits=8)),
                ('a_low', models.DecimalField(decimal_places=3, max_digits=8)),
                ('a_high', models.DecimalField(decimal_places=3, max_digits=8)),
                ('a_fifty_two_week_high', models.DecimalField(decimal_places=3, max_digits=8)),
                ('a_fifty_two_week_low', models.DecimalField(decimal_places=3, max_digits=8)),
                ('a_ask', models.DecimalField(decimal_places=3, max_digits=8)),
                ('q_ask_size', models.IntegerField()),
                ('a_bid', models.DecimalField(decimal_places=3, max_digits=8)),
                ('q_bid_size', models.IntegerField()),
                ('a_two_hundred_day_avg', models.DecimalField(decimal_places=5, max_digits=10)),
                ('a_fifty_day_avg', models.DecimalField(decimal_places=5, max_digits=10)),
                ('a_volume', models.IntegerField()),
                ('a_avg_volume', models.IntegerField()),
                ('a_ten_day_vol_avg', models.IntegerField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_summary.stock')),
            ],
            options={
                'unique_together': {('stock', 'd_process')},
            },
        ),
    ]
