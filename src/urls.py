from django.conf.urls import patterns, url, include, handler404, handler500
from django.contrib import admin
import admin as project_admin

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admind/', include(admin.site.urls)),
    (r'^', include('core.urls')),
)
