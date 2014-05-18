from django.conf.urls import patterns, url, include, handler404, handler500
from django.contrib import admin

import sitemap

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admind/', include(admin.site.urls)),
    (r'^votes/', include('votes.urls')),
    (r'^dynamic_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap.sitemaps}),
    (r'^', include('discounts.urls')),
    (r'^', include('mountains.urls')),
    (r'^', include('movies.urls')),
    (r'^', include('core.urls')),
)
