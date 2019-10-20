# Generated by Django 2.2.5 on 2019-10-19 20:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20191019_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 20, 38, 42, 386919, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 20, 38, 42, 425697, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]
