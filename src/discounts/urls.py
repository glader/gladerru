# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views import *


urlpatterns = patterns('',
    url(r'^discounts/(\d+)/edit$', discount_edit, name='discount_edit'),
    url(r'^discounts/(\d+)/delete$', discount_delete, name='discount_delete'),
    url(r'^discounts/new$', discount_new, name='discount_new'),
    url(r'^discounts/$', discounts, name='discounts'),
)
