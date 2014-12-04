# coding: utf8

from django.contrib.sitemaps import GenericSitemap
from .models import Post, Photo


sitemaps = {
    'post': GenericSitemap({"queryset": Post.objects.all()}, changefreq="weekly"),
    'photo': GenericSitemap({"queryset": Photo.objects.all()}, changefreq="weekly"),
}
