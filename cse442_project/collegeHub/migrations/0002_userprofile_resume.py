# Generated by Django 3.1.2 on 2020-10-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeHub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
