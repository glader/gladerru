# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class MountainPhotoInline(admin.TabularInline):
    model = models.MountainPhoto


class MountainAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_filter = ('region', 'check_date')
    list_display = ('title', 'check_date')
    search_fields = ('slug', 'title')
    inlines = (MountainPhotoInline,)

admin.site.register(models.Mountain, MountainAdmin)
admin.site.register(models.Region)
admin.site.register(models.District)
