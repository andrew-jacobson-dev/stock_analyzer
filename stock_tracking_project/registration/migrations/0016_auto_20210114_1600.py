# Generated by Django 3.1.3 on 2021-01-14 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0015_auto_20210114_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='i_custom_alerts_buy',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_custom_alerts_other',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_custom_alerts_sell',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_custom_alerts_send_email',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_custom_alerts_send_text',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_expert_rec_buy',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_expert_rec_other',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_expert_rec_sell',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_expert_rec_send_email',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_expert_rec_send_text',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_summary_pg_alerts_open',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_summary_pg_port_open',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='i_summary_pg_trans_open',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserSettings',
        ),
    ]
