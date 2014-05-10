# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

from yafotki.fields import YFField
from votes.models import VoteMixin


class Region(models.Model):
    """ Регион """
    title = models.CharField(max_length=250, verbose_name=u"Название")
    order = models.PositiveIntegerField(verbose_name=u"Порядок")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("region", args=[self.id])

    class Meta:
        verbose_name = u"Регион"
        verbose_name_plural = u"Регионы"
        ordering = ['order']


class District(models.Model):
    """ Область """
    title = models.CharField(max_length=250, verbose_name=u"Название")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("district", args=[self.id])

    class Meta:
        verbose_name = u"Область"
        verbose_name_plural = u"Области"


class Mountain(models.Model, VoteMixin):
    name = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name=u"Имя элемента")
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Статус")

    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Адрес")
    district = models.ForeignKey(District, null=True, blank=True, verbose_name=u"Область")
    has_ratrack = models.BooleanField(default=False, verbose_name=u"Есть ратрак")
    hidden = models.BooleanField(default=False, verbose_name=u"Скрытый")
    image = YFField(upload_to="gladerru", null=True, blank=True, verbose_name=u"Схема трасс", default=None)
    lifts = models.TextField(null=True, blank=True, verbose_name=u"Подъемники")
    latitude = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"Широта")
    longitude = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"Долгота")
    longest = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Самая длинная трасса")
    nightwork = models.TextField(null=True, blank=True, verbose_name=u"Ночная работа", help_text=u"До скольки")
    oldschool = models.BooleanField(default=False, verbose_name=u"Олдскул")
    overfall = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Перепад высот")
    pistelength = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Общая длина трасс")
    pistes = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Кол-во трасс")
    prices = models.TextField(null=True, blank=True, verbose_name=u"Цены")
    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    region = models.ForeignKey(Region, verbose_name=u"Регион")
    service = models.TextField(null=True, blank=True, verbose_name=u"Услуги")
    snowpark = models.TextField(null=True, blank=True, verbose_name=u"Сноупарк")
    tel = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Телефоны")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    webcam = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"Web камера")
    work_time = models.TextField(max_length=50, null=True, blank=True, verbose_name=u"Время работы")
    email = models.EmailField(null=True, blank=True, verbose_name=u"Email")

    newbie = models.BooleanField(default=False, verbose_name=u"Есть учебный склон")
    parking = models.BooleanField(default=False, verbose_name=u"Есть платная стоянка")
    rental = models.BooleanField(default=False, verbose_name=u"Есть прокат оборудования")
    room = models.BooleanField(default=False, verbose_name=u"Комната для переодевания")
    safe = models.BooleanField(default=False, verbose_name=u"Есть камера хранения")
    has_service = models.BooleanField(default=False, verbose_name=u"Есть мастерская/сервис")
    cafe = models.BooleanField(default=False, verbose_name=u"Есть кафе")
    hotel = models.TextField(null=True, blank=True, verbose_name=u"Гостиница")
    has_light = models.BooleanField(default=False, verbose_name=u"Есть освещение трасс")
    has_show = models.BooleanField(default=False, verbose_name=u"Искусственный снег")

    check_date = models.DateField(null=True, blank=True, verbose_name=u"Дата обработки")
    proof_url = models.TextField(null=True, blank=True, verbose_name=u"Источник данных")

    def get_absolute_url(self):
        return reverse("mountain", args=[self.name])

    def __unicode__(self):
        return self.title

    @property
    def uid(self):
        return "%s_%s" % (self.__class__.__name__.lower(), self.id)

    class Meta:
        verbose_name = u"Гора"
        verbose_name_plural = u"Горы"


class MountainPhoto(models.Model):
    mountain = models.ForeignKey(Mountain, verbose_name="Гора")
    image = YFField(upload_to='gladerru', verbose_name=u"Картинка")

    class Meta:
        verbose_name = u"Фото горы"
        verbose_name_plural = u"Фото гор"
