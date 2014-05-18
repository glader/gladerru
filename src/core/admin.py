# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models
from django.contrib.auth.models import User, Permission


class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    ordering = ('-date_created',)
    list_display = ('user', 'date_created', 'pub_post_count')
    search_fields = ('user__username',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'author', 'status', 'date_created')
    ordering = ('-date_created',)
    list_filter = ('status',)
    search_fields = ('name', 'title', 'slug', 'url')
    raw_id_fields = ('author',)
    exclude = ('tags',)


class RubricAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    ordering = ('title',)
    search_fields = ('name', 'title')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')


class Tag2SkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'tag')
    raw_id_fields = ('skill', 'tag')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'item', 'date_created')
    ordering = ('-date_created',)
    raw_id_fields = ('author',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'type', 'checked', 'size')
    list_filter = ('type', 'checked')
    search_fields = ('name', 'title')
    raw_id_fields = ('primary_synonim', 'parent')


class WordAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'type', 'abstract', 'has_content')
    ordering = ('title',)
    list_filter = ('type',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author', 'post', 'date_created')
    ordering = ('-date_created',)
    raw_id_fields = ('author', 'post', 'rider', 'photographer')
    exclude = ('tags',)
    search_fields = ('slug', 'title')


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Tag2Skill, Tag2SkillAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Rubric, RubricAdmin)
admin.site.register(models.Word, WordAdmin)
admin.site.register(models.Photo, PhotoAdmin)


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'type', 'url')
    ordering = ('keyword',)
    list_filter = ('type',)
    search_fields = ('keyword', 'url')

admin.site.register(models.Keyword, KeywordAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'email', 'date_joined')
    ordering = ('-date_joined',)
    search_fields = ('username', 'first_name', 'email')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Permission)


class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order')
    prepopulated_fields = {"slug": ("title",)}
    ordering = ('order',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'dt_created')
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ('-dt_created',)

admin.site.register(models.NewsCategory, NewsCategoryAdmin)
admin.site.register(models.News, NewsAdmin)
