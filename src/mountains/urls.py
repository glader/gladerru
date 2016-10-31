# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^mountains/(?P<slug>[^/]+)$', views.MountainView.as_view(), name='mountain'),
    url(r'^mountains$', views.MountainsView.as_view(), name='mountains'),
    url(r'^regions/(?P<pk>\d+)$', views.RegionView.as_view(), name='region'),
]
