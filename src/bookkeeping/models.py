# -*- coding: utf-8 -*-
from django.db import models


class Record(models.Model):
    u"""Запись"""
    ACCOUNTS = (
        ('glader', u'Glader'),
        ('skyslayer', u'Skyslayer'),
    )
    account = models.CharField(verbose_name=u"Аккаунт", choices=ACCOUNTS, max_length=50)
    amount = models.DecimalField(verbose_name=u"Сумма", max_digits=12, decimal_places=2)
    created = models.DateTimeField(verbose_name=u"Добавлено", auto_now_add=True)
    comment = models.TextField(verbose_name=u"Описание")

    class Meta:
        verbose_name = u"Запись"
        verbose_name_plural = u"Записи"
        ordering = ['-created']
