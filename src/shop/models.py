# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    u"""Категории товаров"""
    title = models.CharField(max_length=200, verbose_name=u"Название")
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u"Родитель")
    show_sex = models.BooleanField(default=False, verbose_name=u"Показывать пол")
    amount_of_goods = models.IntegerField(default=0, verbose_name=u"Количество товаров в категории")
    order = models.IntegerField(default=100, verbose_name=u"Порядок")

    def __unicode__(self):
        if self.parent:
            return u"%s > %s" % (self.parent.title, self.title)
        else:
            return self.title

    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"
        ordering = ['order', 'title']


class Brand(models.Model):
    u"""Бренд"""
    title = models.CharField(max_length=200, verbose_name=u"Название")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Бренд"
        verbose_name_plural = u"Бренды"
        ordering = ['title']


class Item(models.Model):
    u"""Товар"""
    category = models.ForeignKey(Category, verbose_name=u"Категория")
    brand = models.ForeignKey(Brand, verbose_name=u"Бренд")
    image = models.CharField(max_length=255, verbose_name=u"Картинка")
    title = models.CharField(max_length=255, verbose_name=u"Название")
    size = models.CharField(max_length=255, verbose_name=u"Размеры", null=True, default=None)
    sex = models.CharField(max_length=255, verbose_name=u"Пол")
    description = models.TextField(verbose_name=u"Описание")
    price = models.CharField(max_length=255, verbose_name=u"Цена")
    url = models.CharField(max_length=255, verbose_name=u"Адрес")
    update = models.DateTimeField(verbose_name=u"Обновлено")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"
        ordering = ['category', 'title']
