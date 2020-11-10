# Generated by Django 3.1.2 on 2020-10-27 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeHub', '0014_auto_20201027_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='certification_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.CharField(default='', max_length=280),
        ),
        migrations.AlterField(
            model_name='education',
            name='institution',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
