# Generated by Django 3.1.3 on 2020-12-27 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_pull', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_run', models.DateField(auto_now_add=True)),
                ('t_job_name', models.CharField(max_length=60)),
                ('t_script_name', models.CharField(max_length=60)),
                ('t_status', models.CharField(max_length=30)),
                ('t_message', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['-d_run', 't_job_name'],
            },
        ),
    ]
