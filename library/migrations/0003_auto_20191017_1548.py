# Generated by Django 2.2.5 on 2019-10-17 12:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20191009_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookitem',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, storage='storages.backends.s3boto3.S3Boto3Storage', upload_to=library.models.photo_upload_path, verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 12, 48, 43, 126490, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 12, 48, 43, 152892, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]
