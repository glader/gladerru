from django.conf.urls import patterns, url, include, handler404, handler500
from django.contrib import admin

urlpatterns = patterns('',
    (r'^admind/', include(admin.site.urls)),
    (r'^', include('core.urls')),
)
