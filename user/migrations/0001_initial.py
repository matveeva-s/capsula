# Generated by Django 2.2.5 on 2019-10-09 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='Email')),
                ('django_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_django', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь django')),
            ],
        ),
    ]
