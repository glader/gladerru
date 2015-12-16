# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from jsonfield.fields import JSONField


class LandingPage(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    template = models.CharField(verbose_name='Шаблон', max_length=100, default='', blank=True)
    slug = models.CharField(verbose_name='Slug', max_length=100)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lp:page', args=[self.slug])

    class Meta:
        verbose_name = 'LP'
        verbose_name_plural = 'LP'


class Stat(models.Model):
    page = models.ForeignKey(LandingPage, verbose_name='Страница')
    params = JSONField(verbose_name='Параметры', default={})
    hash = models.CharField(verbose_name='Хэш', max_length=100)
    views = models.PositiveIntegerField(verbose_name='Просмотров', default=0)
    actions = models.PositiveIntegerField(verbose_name='Действий', default=0)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
