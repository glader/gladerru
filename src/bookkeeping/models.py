# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Record(models.Model):
    """Запись"""
    ACCOUNTS = (
        ('glader', 'Glader'),
        ('skyslayer', 'Skyslayer'),
    )
    account = models.CharField(verbose_name='Аккаунт', choices=ACCOUNTS, max_length=50)
    amount = models.DecimalField(verbose_name='Сумма', max_digits=12, decimal_places=2)
    created = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)
    comment = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created']
