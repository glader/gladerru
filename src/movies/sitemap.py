# coding: utf8

from django.contrib.sitemaps import GenericSitemap
from .models import Man, Movie, Studio


sitemaps = {
    'man': GenericSitemap({"queryset": Man.objects.all()}, changefreq="daily"),
    'movie': GenericSitemap({"queryset": Movie.objects.all()}, changefreq="daily"),
    'studio': GenericSitemap({"queryset": Studio.objects.all()}, changefreq="daily"),
}
