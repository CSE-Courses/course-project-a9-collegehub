# Generated by Django 3.0.4 on 2020-10-26 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collegeHub', '0011_auto_20201026_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='education', to='collegeHub.UserProfile'),
        ),
    ]
