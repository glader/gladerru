# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views.admin import *
from views.content import *
from views.ugc import *
from feeds import *
from django.contrib.auth.views import password_reset


urlpatterns = patterns('',
    url(r'^content/([^/]+)\.htm$', article, name='article'),
    url(r'^rubric/([^/]+)$', rubric, name='rubric'),

    url(r'^(ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video)$', category_view, name='category'),
    url(r'^(ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video)/(\d+)$', post_view, name='post'),

    url(r'^terms/([^/]+)$', dictionary_word, name='dictionary_word'),
    url(r'^terms/', dictionary, name='dictionary'),
    url(r'^skills/([^/]+)$', skill, name='skill'),
    url(r'^skills/$', skills, name='skills'),
    url(r'^tricks/([^/]+)$', trick, name='trick'),
    url(r'^tricks/$', tricks, name='tricks'),
    url(r'^search', search, name='search'),
    url(r'^feedback', feedback, name='feedback'),

    url(r'^auth/login$', login, name='login'),
    url(r'^auth/registration$', registration, name='registration'),
    url(r'^auth/logout$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^auth/reset$', password_reset, name='password_reset'),
    url(r'^auth/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^auth/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^auth/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # Ajax
    url(r'^ajax/add_photo$', add_photo, name='add_photo'),
    url(r'^crossdomain.xml$', crossdomain, name='crossdomain'),
    url(r'^ajax/tags_suggest', tags_suggest),
    url(r'^ajax/upload_photo$', 'core.views.admin.upload_photos', name='upload_photos'),

    # Feeds
    (r'^feeds/all', AllPosts()),

    # Editing
    url(r'^post/new$', new_post, name='new_post'),
    url(r'^post/edit/(\d+)$', edit_post, name='edit_post'),

    url(r'^$', index, name='index'),

    # Old urls
    url(r'^users/([^/]+)/posts/(\d+)$', user_post),
)
