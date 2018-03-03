# Generated by Django 2.0.1 on 2018-03-03 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('value', models.IntegerField(default=1)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discussions.Comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=280),
        ),
        migrations.AddField(
            model_name='vote',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discussions.Post'),
        ),
        migrations.AddField(
            model_name='vote',
            name='topic_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_post', to='discussions.Post'),
        ),
        migrations.AddField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
