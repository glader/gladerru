# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views import *


urlpatterns = patterns('',
    url(r'^mountains/([^/]+)$', mountain, name='mountain'),
    url(r'^mountains/$', mountains, name='mountains'),
    url(r'^regions/(\d+)$', region, name='region'),
)
