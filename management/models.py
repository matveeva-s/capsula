from django.db import models

from library.models import Book
from user.models import User


class ComplaintBook(models.Model):
    UNREAL = 0
    INSULT = 1
    ABSENT = 2
    ERROR = 3
    OTHER = 4

    COMPLAINT_BOOK_REASONS = (
        (UNREAL, 'Книга не существует'),
        (INSULT, 'Оскорбительное содержание'),
        (ABSENT, 'Книга отсутствует у владельца'),
        (ERROR, 'Неправильное описание'),
        (OTHER, 'Другое')
    )

    NEW = 31
    VALID = 32
    INVALID = 33

    COMPLAINT_BOOK_STATUSES = (
        (NEW, 'Новая'),
        (VALID, 'Правильная'),
        (INVALID, 'Ложная')
    )

    author = models.ForeignKey(
        User, related_name='complaint_book_author', verbose_name='Автор жалобы',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    content = models.IntegerField(verbose_name='Причина жалобы на книгу', choices=COMPLAINT_BOOK_REASONS)
    book = models.ForeignKey(Book, verbose_name='Книга в жалобе', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    status = models.IntegerField(verbose_name='Статус жалобы на книгу', choices=COMPLAINT_BOOK_STATUSES)

    class Meta:
        verbose_name = 'Жалобы на книги'
        verbose_name_plural = 'Жалобы-Книги'
        ordering = ('pk',)

    def __str__(self):
        return self.book.title


class ComplaintUser(models.Model):
    UNREAL = 0
    INSULT = 1
    OTHER = 2

    COMPLAINT_USER_REASONS = (
        (UNREAL, 'Не существует'),
        (INSULT, 'Оскорбительное поведение'),
        (OTHER, 'Другое')
    )

    NEW = 31
    VALID = 32
    INVALID = 33

    COMPLAINT_USER_STATUSES = (
        (NEW, 'Новая'),
        (VALID, 'Правильная'),
        (INVALID, 'Ложная')
    )

    author = models.ForeignKey(
        User, related_name='complaint_user_author', verbose_name='Автор жалобы',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    content = models.IntegerField(verbose_name='Причина жалобы на пользователя', choices=COMPLAINT_USER_REASONS)
    user = models.ForeignKey(User, verbose_name='Пользователь в жалобе', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    status = models.IntegerField(verbose_name='Статус жалобы на пользователя', choices=COMPLAINT_USER_STATUSES)

    class Meta:
        verbose_name = 'Жалобы на ользователей'
        verbose_name_plural = 'Жалобы-Пользователи'
        ordering = ('pk',)

    def __str__(self):
        return self.user.first_name
