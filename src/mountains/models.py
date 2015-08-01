# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

from yafotki.fields import YFField
from votes.models import VoteMixin


class Region(models.Model):
    """ Регион """
    title = models.CharField(max_length=250, verbose_name='Название')
    order = models.PositiveIntegerField(verbose_name='Порядок')
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('region', args=[self.id])

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['order']


class District(models.Model):
    """ Область """
    title = models.CharField(max_length=250, verbose_name='Название')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('district', args=[self.id])

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'


class Mountain(models.Model, VoteMixin):
    slug = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name='Код горы')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='Название')
    content = models.TextField(null=True, blank=True, verbose_name='Содержание элемента')
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name='Статус')

    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Адрес')
    district = models.ForeignKey(District, null=True, blank=True, verbose_name='Область')
    has_ratrack = models.BooleanField(default=False, verbose_name='Есть ратрак')
    hidden = models.BooleanField(default=False, verbose_name='Скрытый')
    image = YFField(upload_to='gladerr', null=True, blank=True, verbose_name='Схема трасс', default=None)
    lifts = models.TextField(null=True, blank=True, verbose_name='Подъемники')
    latitude = models.CharField(max_length=20, null=True, blank=True, verbose_name='Широта')
    longitude = models.CharField(max_length=20, null=True, blank=True, verbose_name='Долгота')
    longest = models.CharField(max_length=50, null=True, blank=True, verbose_name='Самая длинная трасса')
    nightwork = models.TextField(null=True, blank=True, verbose_name='Ночная работа', help_text='До скольки')
    oldschool = models.BooleanField(default=False, verbose_name='Олдскул')
    overfall = models.CharField(max_length=50, null=True, blank=True, verbose_name='Перепад высот')
    pistelength = models.CharField(max_length=50, null=True, blank=True, verbose_name='Общая длина трасс')
    pistes = models.CharField(max_length=50, null=True, blank=True, verbose_name='Кол-во трасс')
    prices = models.TextField(null=True, blank=True, verbose_name='Цены')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    region = models.ForeignKey(Region, verbose_name='Регион')
    service = models.TextField(null=True, blank=True, verbose_name='Услуги')
    snowpark = models.TextField(null=True, blank=True, verbose_name='Сноупарк')
    tel = models.CharField(max_length=250, null=True, blank=True, verbose_name='Телефоны')
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name='URL')
    webcam = models.URLField(max_length=250, null=True, blank=True, verbose_name='Web камера')
    work_time = models.TextField(max_length=50, null=True, blank=True, verbose_name='Время работы')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    interactive_map = models.TextField(verbose_name='Интеракт. карта', null=True, blank=True, default=None)

    newbie = models.BooleanField(default=False, verbose_name='Есть учебный склон')
    parking = models.BooleanField(default=False, verbose_name='Есть платная стоянка')
    rental = models.BooleanField(default=False, verbose_name='Есть прокат оборудования')
    room = models.BooleanField(default=False, verbose_name='Комната для переодевания')
    safe = models.BooleanField(default=False, verbose_name='Есть камера хранения')
    has_service = models.BooleanField(default=False, verbose_name='Есть мастерская/сервис')
    cafe = models.BooleanField(default=False, verbose_name='Есть кафе')
    hotel = models.TextField(null=True, blank=True, verbose_name='Гостиница')
    has_light = models.BooleanField(default=False, verbose_name='Есть освещение трасс')
    has_show = models.BooleanField(default=False, verbose_name='Искусственный снег')

    check_date = models.DateField(null=True, blank=True, verbose_name='Дата обработки')
    proof_url = models.TextField(null=True, blank=True, verbose_name='Источник данных')
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)

    def get_absolute_url(self):
        return reverse('mountain', args=[self.slug])

    def __unicode__(self):
        return self.title

    @property
    def uid(self):
        return '%s_%s' % (self.__class__.__name__.lower(), self.id)

    class Meta:
        verbose_name = 'Гора'
        verbose_name_plural = 'Горы'


class MountainPhoto(models.Model):
    mountain = models.ForeignKey(Mountain, verbose_name='Гора')
    image = YFField(upload_to='gladerr', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Фото горы'
        verbose_name_plural = 'Фото гор'
