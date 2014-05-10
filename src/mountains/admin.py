# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class MountainPhotoInline(admin.TabularInline):
    model = MountainPhoto


class MountainAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_filter = ('region', 'check_date')
    list_display = ('title', 'check_date')
    search_fields = ('name', 'title')
    inlines = (MountainPhotoInline,)

admin.site.register(Mountain, MountainAdmin)
admin.site.register(Region)
admin.site.register(District)
