# coding: utf-8
from django.contrib.sitemaps import GenericSitemap

from mountains.models import Mountain

sitemaps = {
    'mountain': GenericSitemap({'queryset': Mountain.objects.all()}, changefreq='weekly'),
}
