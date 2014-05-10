# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Discount(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Пользователь")
    city = models.CharField(verbose_name=u"Город", max_length=200)
    card = models.CharField(verbose_name=u"Карточка", max_length=200)
    discount = models.CharField(verbose_name=u"Скидка", max_length=20)
    contacts = models.TextField(verbose_name=u"Контакты", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)

    def __unicode__(self):
        return "%s %s" % (self.card, self.discount)

    class Meta:
        verbose_name = u"Дисконтная карта"
        verbose_name_plural = u"Дисконтные карты"
