# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views import *


urlpatterns = patterns('',
    url(r'^add_post_vote$', add_post_vote, name='add_post_vote'),
)
