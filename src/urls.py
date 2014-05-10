from django.conf.urls import patterns, url, include, handler404, handler500
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admind/', include(admin.site.urls)),
    (r'^votes/', include('votes.urls')),
    (r'^', include('core.urls')),
)
