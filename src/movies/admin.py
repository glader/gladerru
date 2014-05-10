# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class SongAdmin(admin.ModelAdmin):
    list_display = ('movie', 'performer', 'title', 'note', 'order')
    search_fields = ('movie', 'performer', 'title')
    raw_id_fields = ('movie',)


class ManAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'hidden')
    ordering = ('title',)
    search_fields = ('slug', 'title', 'content')
    list_filter = ('hidden',)
    raw_id_fields = ('primary_synonim',)


class StudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    ordering = ('title',)
    search_fields = ('slug', 'title')


class Man2MovieInline(admin.TabularInline):
    model = Man2Movie
    raw_id_fields = ('man',)
    extra = 0


class SongInline(admin.TabularInline):
    model = Song
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Profile field', {
            'fields': ('title', 'slug', 'studio', 'year', 'content', 'teaser', 'full_movie',
                       'torrent', 'url', 'cover',
                       )
        }),
        ('Additional', {'fields': ('has_songs', 'rating', 'tag', 'hidden'), 'classes': ('collapse',)})
    )

    list_display = ('title', 'studio', 'year')
    ordering = ('-year', 'title')
    raw_id_fields = ('studio',)
    search_fields = ('slug', 'title')
    inlines = (Man2MovieInline, SongInline)


class PictureBoxAdmin(admin.ModelAdmin):
    list_display = ('picture', 'user', 'action', 'dt')
    ordering = ('-dt',)


admin.site.register(Song, SongAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Man, ManAdmin)
admin.site.register(Studio, StudioAdmin)
admin.site.register(PictureBox, PictureBoxAdmin)
