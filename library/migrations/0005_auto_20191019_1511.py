# Generated by Django 2.2.5 on 2019-10-19 12:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20191019_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 12, 11, 16, 738822, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 19, 12, 11, 16, 771620, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]