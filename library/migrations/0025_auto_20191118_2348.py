# Generated by Django 2.2.5 on 2019-11-18 20:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0024_auto_20191111_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.CharField(max_length=150, null=True, unique=True, verbose_name='URL картинки'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 20, 48, 12, 578718, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='status',
            field=models.IntegerField(choices=[(0, 'Заявка рассматривается'), (1, 'Заявка принята, книга ожидает передачи'), (2, 'Заявка отклонена'), (3, 'Книга читается'), (4, 'Книга возвращена'), (5, 'Завяка отменена')], verbose_name='Статус обмена'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 20, 48, 12, 605772, tzinfo=utc), verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 20, 48, 12, 606636, tzinfo=utc), verbose_name='Дата создания'),
        ),
    ]
