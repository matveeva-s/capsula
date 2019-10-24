# Generated by Django 2.2.5 on 2019-10-19 19:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20191019_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 19, 54, 33, 794681, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 19, 54, 33, 826551, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]