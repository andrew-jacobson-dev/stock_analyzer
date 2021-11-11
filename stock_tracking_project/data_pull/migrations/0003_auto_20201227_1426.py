# Generated by Django 3.1.3 on 2020-12-27 13:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data_pull', '0002_jobrun'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobrun',
            options={'ordering': ['-s_run', 't_job_name']},
        ),
        migrations.RemoveField(
            model_name='jobrun',
            name='d_run',
        ),
        migrations.AddField(
            model_name='jobrun',
            name='s_run',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
