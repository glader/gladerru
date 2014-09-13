# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.Overview.as_view(), name='bookkeeping_index'),
)
