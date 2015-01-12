# -*- coding: utf-8 -*-
from django.contrib import admin

from sape import models


class LinkAdmin(admin.ModelAdmin):
    list_display = ('txt', 'url', 'page')
    ordering = ('page',)
    search_fields = ('page', 'url')


admin.site.register(models.Link, LinkAdmin)
