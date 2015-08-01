# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from sape import models


class LinkAdmin(admin.ModelAdmin):
    list_display = ('txt', 'url', 'page')
    ordering = ('page',)
    search_fields = ('page', 'url')


admin.site.register(models.Link, LinkAdmin)
