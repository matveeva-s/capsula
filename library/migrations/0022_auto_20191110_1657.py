# Generated by Django 2.2.5 on 2019-11-10 13:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_auto_20191108_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.IntegerField(choices=[(0, 'Классическая русская литература'), (1, 'Классическая зарубежная литература'), (2, 'Наука и образование'), (10, 'Бизнес-литература и саморазвитие'), (3, 'Компьютерная литература'), (4, 'Учебная литература'), (5, 'Современная проза'), (6, 'Приключения'), (7, 'Фэнтези и фантастика'), (8, ' Ужасы, мистика'), (9, 'Детективы'), (11, 'Книги по психологии'), (12, 'Красота и здоровье'), (13, 'Словари, справочники'), (14, 'Поэзия и драматургия'), (15, 'Комиксы, манга'), (16, 'Дом, семья, хобби и досуг'), (17, 'Культура и искусство'), (18, 'Эротика и секс, любовные романы'), (19, 'Детские книги'), (20, 'Религия'), (21, 'Периодические издания, газеты и журналы'), (22, 'Роман'), (23, 'Научная фантастика')], verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 10, 13, 57, 54, 774343, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 10, 13, 57, 54, 887500, tzinfo=utc), verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 10, 13, 57, 54, 888343, tzinfo=utc), verbose_name='Дата создания'),
        ),
    ]
