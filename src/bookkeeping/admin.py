# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from . import models


class RecordAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'created')


admin.site.register(models.Record, RecordAdmin)
