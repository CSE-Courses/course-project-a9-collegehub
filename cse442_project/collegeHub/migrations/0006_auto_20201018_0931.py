# Generated by Django 3.0.4 on 2020-10-18 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collegeHub', '0005_auto_20201018_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='experiences',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section', to='collegeHub.Experiences'),
        ),
    ]
