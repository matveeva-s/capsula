from django.db import models

# Create your models here.
from user.models import User


class GeoPoint(models.Model):

    user = models.ForeignKey(
        User, related_name='user_map', verbose_name='Пользователь',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    name = models.CharField('Имя', max_length=30, blank=True)
    latitude = models.DecimalField('широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField('долгота', max_digits=9, decimal_places=6)


    class Meta:
        verbose_name = 'Адреса'
        verbose_name_plural = 'Адреса'
        ordering = ('pk',)

    def __str__(self):
        return self.user.first_name