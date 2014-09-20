# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class Man2MovieInline(admin.TabularInline):
    model = models.Man2Movie
    raw_id_fields = ('man', 'movie')
    extra = 0


class SongInline(admin.TabularInline):
    model = models.Song
    extra = 0


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
    inlines = (Man2MovieInline,)


class StudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    ordering = ('title',)
    search_fields = ('slug', 'title')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'studio', 'year')
    ordering = ('-year', 'title')
    raw_id_fields = ('studio',)
    search_fields = ('slug', 'title')
    inlines = (Man2MovieInline, SongInline)
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'studio', 'year', 'teaser')}),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('full_movie', 'content', 'url', 'torrent', 'has_songs', 'cover', 'rating',
                       'dt_teaser_added', 'dt_fullmovie_added', 'dt_soundtrack_added', 'meta_description')}),
    )


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'photographer', 'rating')


admin.site.register(models.Song, SongAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Man, ManAdmin)
admin.site.register(models.Studio, StudioAdmin)
admin.site.register(models.Photo, PhotoAdmin)
