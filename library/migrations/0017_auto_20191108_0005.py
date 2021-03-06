# Generated by Django 2.2.5 on 2019-11-07 21:05

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_merge_20191021_2228'),
        ('library', '0016_auto_20191028_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 21, 5, 37, 922581, tzinfo=utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 21, 5, 37, 951815, tzinfo=utc), verbose_name='Дата изменения'),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 11, 7, 21, 5, 37, 952572, tzinfo=utc), verbose_name='Дата создания')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book', verbose_name='Книга в вишлисте')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.User', verbose_name='Пользователб')),
            ],
            options={
                'verbose_name': 'Вишлист',
                'verbose_name_plural': 'Вишлист',
                'ordering': ('pk',),
            },
        ),
    ]
