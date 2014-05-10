# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group, Permission


class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    ordering = ('-date_created',)
    list_display = ('user', 'date_created', 'pub_post_count')
    search_fields = ('user__username',)


class NewsAdmin(admin.ModelAdmin):
    ordering = ('-date_created',)
    list_display = ('type', 'date_created')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'author', 'status', 'date_created')
    ordering = ('-date_created',)
    list_filter = ('status',)
    search_fields = ('name', 'title')
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


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'card', 'discount', 'contacts', 'date_created')
    ordering = ('-date_created',)
    raw_id_fields = ('user',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Tag2Skill, Tag2SkillAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Post, PostAdmin)
admin.site.register(Rubric, RubricAdmin)


class MountainPhotoInline(admin.TabularInline):
    model = MountainPhoto


class MountainAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_filter = ('region', 'check_date')
    list_display = ('title', 'check_date')
    raw_id_fields = ('root_tag',)
    search_fields = ('name', 'title')
    inlines = (MountainPhotoInline,)

admin.site.register(Mountain, MountainAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Discount, DiscountAdmin)


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'type', 'url')
    ordering = ('keyword',)
    list_filter = ('type',)
    search_fields = ('keyword', 'url')

admin.site.register(Keyword, KeywordAdmin)


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

admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(News, NewsAdmin)
