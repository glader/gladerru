# coding: utf-8
from django.contrib.sitemaps import GenericSitemap

from movies.models import Man, Movie, Studio

sitemaps = {
    'man': GenericSitemap({'queryset': Man.objects.all()}, changefreq='monthly'),
    'movie': GenericSitemap({'queryset': Movie.objects.all()}, changefreq='monthly'),
    'studio': GenericSitemap({'queryset': Studio.objects.all()}, changefreq='monthly'),
}
