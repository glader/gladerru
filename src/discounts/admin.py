# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Discount


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'card', 'discount', 'contacts', 'date_created')
    ordering = ('-date_created',)
    raw_id_fields = ('user',)

admin.site.register(Discount, DiscountAdmin)
