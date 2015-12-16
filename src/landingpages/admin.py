# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from landingpages import models


@admin.register(models.LandingPage)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('page', 'params', 'views', 'actions')
    ordering = ('page', 'params')
    list_filter = ('page',)
    raw_id_fields = ('page',)
    search_fields = ('hash',)
