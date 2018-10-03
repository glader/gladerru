# coding: utf-8
from django.contrib.sitemaps import GenericSitemap

from core import models

sitemaps = {
    'post': GenericSitemap({'queryset': models.Post.objects.filter(type='post').order_by('id')}, changefreq='monthly'),
    'rubric': GenericSitemap({'queryset': models.NewsCategory.objects.all().order_by('id')}, changefreq='daily'),
    'skill': GenericSitemap({'queryset': models.Skill.objects.all().order_by('id')}, changefreq='daily'),
}
