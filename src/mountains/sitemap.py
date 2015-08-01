# coding: utf8
from __future__ import unicode_literals
from django.contrib.sitemaps import GenericSitemap

from .models import Mountain


sitemaps = {
    'mountain': GenericSitemap({'queryset': Mountain.objects.all()}, changefreq='weekly'),
}
