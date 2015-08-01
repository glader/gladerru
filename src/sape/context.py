# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.safestring import mark_safe

from sape.models import Link


def links(request):
    page_links = Link.objects.filter(status__in=('OK', 'ERROR'), page=request.META['PATH_INFO'])
    return {'sape_links': mark_safe(u', '.join(map(unicode, page_links)))}
