from django.contrib.auth.models import User as DjangoUser
from django.core.files.storage import FileSystemStorage
from django.db import models

from capsula import settings


class OverwriteStorage(FileSystemStorage):
    """This class controls that new file upload with same name will overwrite old file"""
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def photo_upload_path(instance, *args, **kwargs):
    """Generates upload path for ImageField/FileField"""
    name = '%s.jpg' % str(instance.id)
    location = 'avatar/%s' % name
    return location


class User(models.Model):

    django_user = models.ForeignKey(
        DjangoUser, related_name='user_django', verbose_name='Пользователь django',
        blank=True, null=True, on_delete=models.CASCADE
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    email = models.EmailField('Email', max_length=150, unique=True)
    avatar = models.CharField('URL аватара', max_length=150, unique=True, blank=False, null=True)
    contact = models.TextField('Контакты', max_length=150, blank=True, null=True)

    books_taken = models.IntegerField('Книг взято', default=0)
    books_given = models.IntegerField('Книг отдано', default=0)

    #delete = models.BooleanField('Удален', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)

    def __str__(self):
        return self.django_user.username


class UserSubscription(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь в рассылке', on_delete=models.CASCADE)
    email_notification = models.BooleanField('Почтовые уведомления', default=True)
    email_news = models.BooleanField('Почтовая рассылка', default=True)
    vk_notification = models.BooleanField('ВК уведомления', default=True)

    class Meta:
        verbose_name = 'Рассылки пользователей'
        verbose_name_plural = 'Рассылки'
        ordering = ('pk',)

    def __str__(self):
        return self.user.first_name
