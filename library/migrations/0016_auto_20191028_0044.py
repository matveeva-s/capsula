# Generated by Django 2.2.5 on 2019-10-27 21:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_auto_20191022_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 27, 21, 44, 0, 420268, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 27, 21, 44, 0, 452251, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]
