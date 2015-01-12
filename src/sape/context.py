# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from sape.models import Link


def links(request):
    page_links = Link.objects.filter(status='OK', page=request.META['PATH_INFO'])
    return {'sape_links': mark_safe(u', '.join(map(unicode, page_links)))}
