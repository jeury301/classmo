# Generated by Django 2.0.1 on 2018-03-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=999999999, max_length=128),
            preserve_default=False,
        ),
    ]