# coding: utf-8
from django.contrib.sitemaps import GenericSitemap

from core import models

sitemaps = {
    'post': GenericSitemap({'queryset': models.Post.objects.filter(type='post')}, changefreq='monthly'),
    'rubric': GenericSitemap({'queryset': models.NewsCategory.objects.all()}, changefreq='daily'),
    'skill': GenericSitemap({'queryset': models.Skill.objects.all()}, changefreq='daily'),
}
