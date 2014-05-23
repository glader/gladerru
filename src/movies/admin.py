# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


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
    model = models.Man2Movie
    raw_id_fields = ('man',)
    extra = 0


class SongInline(admin.TabularInline):
    model = models.Song
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


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'rider', 'photographer')


admin.site.register(models.Song, SongAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Man, ManAdmin)
admin.site.register(models.Studio, StudioAdmin)
admin.site.register(models.PictureBox, PictureBoxAdmin)
admin.site.register(models.Photo, PhotoAdmin)
