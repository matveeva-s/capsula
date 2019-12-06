# Generated by Django 2.2.5 on 2019-12-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20191125_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.AddField(
            model_name='user',
            name='books_given',
            field=models.IntegerField(default=0, verbose_name='Книг отдано'),
        ),
        migrations.AddField(
            model_name='user',
            name='books_taken',
            field=models.IntegerField(default=0, verbose_name='Книг взято'),
        ),
        migrations.AddField(
            model_name='user',
            name='delete',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
    ]
