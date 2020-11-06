# Generated by Django 3.1.3 on 2020-11-04 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeHub', '0024_auto_20201104_0528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(help_text='Day of the event', verbose_name='Day of the event')),
                ('start_time', models.TimeField(help_text='Starting time', verbose_name='Starting time')),
                ('end_time', models.TimeField(help_text='Final time', verbose_name='Final time')),
                ('notes', models.TextField(blank=True, help_text='Textual Notes', null=True, verbose_name='Textual Notes')),
            ],
            options={
                'verbose_name': 'Scheduling',
                'verbose_name_plural': 'Scheduling',
            },
        ),
        migrations.DeleteModel(
            name='IndividualScheduler',
        ),
    ]
