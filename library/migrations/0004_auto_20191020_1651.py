# Generated by Django 2.2.5 on 2019-10-20 13:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20191017_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookitem',
            name='image',
            field=models.CharField(max_length=150, null=True, unique=True, verbose_name='URL картинки'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 20, 13, 51, 12, 88074, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 20, 13, 51, 12, 156591, tzinfo=utc), verbose_name='Дата изменения'),
        ),
    ]
