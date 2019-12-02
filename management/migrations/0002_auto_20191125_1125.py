# Generated by Django 2.2.5 on 2019-11-25 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaintbook',
            name='content',
            field=models.IntegerField(choices=[(0, 'Книга не существует'), (1, 'Оскорбительное содержание'), (2, 'Книга отсутствует у владельца'), (3, 'Неправильное описание'), (4, 'Другое')], verbose_name='Причина жалобы на книгу'),
        ),
    ]