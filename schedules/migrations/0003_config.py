# Generated by Django 2.0.1 on 2018-04-14 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_auto_20180331_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(default='', max_length=128)),
                ('primary_color', models.CharField(default='', max_length=128)),
                ('secondary_color', models.CharField(default='', max_length=128)),
                ('logo', models.CharField(default='', max_length=128)),
                ('slogan', models.CharField(default='', max_length=128)),
                ('font_family', models.CharField(default='', max_length=128)),
                ('welcome_title', models.CharField(default='', max_length=128)),
                ('welcome_body', models.CharField(default='', max_length=128)),
                ('all_courses_body', models.CharField(default='', max_length=128)),
                ('my_courses_body', models.CharField(default='', max_length=128)),
                ('discussion_body', models.CharField(default='', max_length=128)),
                ('secondary_text_color', models.CharField(default='', max_length=1280)),
                ('jumbotron_color', models.CharField(default='', max_length=1280)),
                ('splash_url_1', models.CharField(default='', max_length=1280)),
                ('splash_url_2', models.CharField(default='', max_length=1280)),
                ('splash_url_3', models.CharField(default='', max_length=1280)),
                ('splash_license_1', models.CharField(default='', max_length=1280)),
                ('splash_license_2', models.CharField(default='', max_length=1280)),
                ('splash_license_3', models.CharField(default='', max_length=1280)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
