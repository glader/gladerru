# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^discounts/(\d+)/edit$', views.discount_edit, name='discount_edit'),
    url(r'^discounts/(\d+)/delete$', views.discount_delete, name='discount_delete'),
    url(r'^discounts/new$', views.discount_new, name='discount_new'),
    url(r'^discounts/$', views.discounts, name='discounts'),
)