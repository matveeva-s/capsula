from django.db import models
from django.core import validators


class User(models.Model):

    username = models.CharField(
        'Имя пользователя', max_length=30, unique=True,
        help_text='Обязательное. Не более 30 символов.',
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                (
                    'Введите имя пользователя. '
                    'Может содержать только буквы, цифры и '
                    'символы @/./+/-/_'
                ), 'invalid'
            ),
        ],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        }
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    email = models.EmailField('Email', max_length=150, unique=True)
    password = models.CharField('Пароль', max_length=30, blank=True)

    def __str__(self):
        return self.username
