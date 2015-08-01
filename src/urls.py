from __future__ import unicode_literals
from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings

import sitemap

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admind/', include(admin.site.urls)),
    (r'^redactor/', include('redactor.urls')),
    (r'^votes/', include('votes.urls')),
    (r'^bookkeeping/', include('bookkeeping.urls')),
    (r'^dynamic_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap.sitemaps}),
    (r'^', include('discounts.urls')),
    (r'^', include('mountains.urls')),
    (r'^', include('movies.urls')),
    (r'^', include('core.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
