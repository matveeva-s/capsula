from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def add_swap(email):
    subject = 'Новая заявка'
    message = ' Новая заявка на обмен! \n Заходи на сайт и узнай, кто хочет взять у тебя книгу \n https://www.bookovsky.ru/owner '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    return email


@shared_task
def confirm_swap(email):
    subject = 'Заявка подтверждена'
    message = ' Заявка была одобрена. \n Заходи на сайт и узнай контактные данные владельца книги \n https://www.bookovsky.ru/reader '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    return email


@shared_task
def reject_swap(email):
    subject = 'Заявка отклонена'
    message = ' Заявка была отклонена. \n Заходи на сайт и возможно ты найдешь еще что-то интересное \n https://www.bookovsky.ru '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    return email


