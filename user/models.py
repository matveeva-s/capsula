from django.contrib.auth.models import User as DjangoUser
from django.db import models


def photo_upload_path(instance, *args, **kwargs):
    """Generates upload path for ImageField/FileField"""
    name = '%s.jpg' % (str(instance.id),)
    location = 'avatar/%s' % (name,)
    return location


class User(models.Model):

    django_user = models.ForeignKey(
        DjangoUser, related_name='user_django', verbose_name='Пользователь django',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    email = models.EmailField('Email', max_length=150, unique=True)
    avatar = models.ImageField(
        verbose_name='Аватар', upload_to=photo_upload_path, default='', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)

    def __str__(self):
        return self.django_user.username
