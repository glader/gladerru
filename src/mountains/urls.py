# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^mountains/([^/]+)$', views.mountain, name='mountain'),
    url(r'^mountains/$', views.mountains, name='mountains'),
    url(r'^regions/(\d+)$', views.region, name='region'),
)
