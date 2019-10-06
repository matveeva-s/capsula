from django.contrib.auth.models import User
from django.db import models


class User(models.Model):

    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    email = models.EmailField('Email', max_length=150, unique=True)
    django_user = models.ForeignKey(
        User, related_name='user_django', verbose_name='Пользователь django',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.email
