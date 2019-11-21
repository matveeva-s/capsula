from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def add_swap(str):
    subject = 'Новая заявка'
    message = ' Новая заявка на обмен! '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ivanova.ev@phystech.edu', ]
    send_mail(subject, message, email_from, recipient_list)
    return str


