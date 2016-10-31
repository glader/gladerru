from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as sitemap_view

import sitemap

admin.autodiscover()

urlpatterns = [
    url(r'^admind/', include(admin.site.urls)),
    url(r'^bookkeeping/', include('bookkeeping.urls')),
    url(r'^dynamic_sitemap\.xml$', sitemap_view, {'sitemaps': sitemap.sitemaps}),
    url(r'^lp/', include('landingpages.urls', namespace='lp')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^', include('discounts.urls')),
    url(r'^', include('mountains.urls')),
    url(r'^', include('movies.urls')),
    url(r'^', include('core.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
