# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^add_post_vote$', views.add_post_vote, name='add_post_vote'),
)