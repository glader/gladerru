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
    url(r'^tags/(.+)$', tag, name='tags'),
    url(r'^tags', tags, name='tags_all'),
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

    url(r'^reports/memcache$', memcache_report, name='reports_memcache'),
    url(r'^reports/404', observe_404),
    url(r'^reports/timing', timing_report, name='reports_timing'),
    url(r'^reports$', reports, name='reports'),

    # UGC
    url(r'^all$', all, name='all'),
    url(r'^top/comments$', top_discussed, name='top_discussed'),
    url(r'^top/best$', top_rating, name='top_rating'),
    url(r'^faq$', faq, name='faq'),
    url(r'^users/(?P<username>[\w\.-]+)/?$', user_profile, name='profile'),
    url(r'^users/(?P<username>[\w\.-]+)/posts/?$', user_posts, name='user_posts'),
    url(r'^users/(?P<username>[\w\.-]+)/(?P<section>[\w]+)/?$', user_staff, name='user_staff'),
    url(r'^users/(?P<username>[\w\.-]+)/(?P<section>[\w]+)/(?P<item_id>[\d]+)/?$', user_item, name='user_item'),

    url(r'^my$', my_profile, name='my_profile'),
    url(r'^my/drafts$', drafts, name='drafts'),
    url(r'^my/settings$', my_settings, name='settings'),

    # Ajax
    url(r'^ajax/add_photo$', add_photo, name='add_photo'),
    url(r'^ajax/set_name$', set_name, name='set_name'),
    url(r'^ajax/set_news$', set_news, name='set_news'),
    url(r'^crossdomain.xml$', crossdomain, name='crossdomain'),
    url(r'^ajax/tags_suggest', tags_suggest),
    url(r'^ajax/upload_photo$', 'core.views.admin.upload_photos', name='upload_photos'),

    # Feeds
    (r'^feeds/best$', BestPosts()),
    (r'^feeds/all', AllPosts()),
    (r'^feeds/tags/(?P<tag_name>.+)$', Tags()),

    # Editing
    url(r'^post/new$', new_post, name='new_post'),
    url(r'^post/edit/(\d+)$', edit_post, name='edit_post'),
    url(r'^photo/edit/(\d+)$', edit_photo, name='edit_photo'),
    url(r'^editprofile$', editprofile, name='editprofile'),
    url(r'^editpassword$', editpassword, name='editpassword'),

    url(r'^$', index, name='index'),

    # Create new elements
    url(r'^create/tag_replace$', tag_replace, name='tag_replace'),

    url(r'^hidden$', hidden, name='hidden'),
)
