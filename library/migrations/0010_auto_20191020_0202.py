# Generated by Django 2.2.5 on 2019-10-19 23:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20191019_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 23, 2, 16, 939954, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 23, 2, 16, 977539, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]