# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import ItemVote


class ItemVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'vote', 'date_created')
    ordering = ('-date_created',)
    raw_id_fields = ('user',)


admin.site.register(ItemVote, ItemVoteAdmin)
