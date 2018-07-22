# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from core.views.content import *
from core.views.ugc import *
from core.feeds import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^(?P<slug>ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video)$',
        CategoryView.as_view(),
        name='category'),
    url(r'^(content|ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video|other)/([^\s]+).htm$',
        PostView.as_view(), name='post'),

    url(r'^terms/(?P<slug>[^/]+)$', DictionaryWordView.as_view(), name='dictionary_word'),
    url(r'^terms/', DictionaryView.as_view(), name='dictionary'),
    url(r'^skills/(?P<slug>[^/]+)$', SkillView.as_view(), name='skill'),
    url(r'^skills/$', SkillsView.as_view(), name='skills'),
    url(r'^tricks/(?P<slug>[^/]+)$', TrickView.as_view(), name='trick'),
    url(r'^tricks/$', TricksView.as_view(), name='tricks'),
    url(r'^search', SearchView.as_view(), name='search'),
    url(r'^feedback', FeedbackView.as_view(), name='feedback'),

    url(r'^auth/login$', LoginView.as_view(), name='login'),
    url(r'^auth/registration$', RegistrationView.as_view(), name='registration'),
    url(r'^auth/logout$', auth_views.logout, name='logout'),
    url(r'^auth/reset$', auth_views.password_reset, name='password_reset'),
    url(r'^auth/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^auth/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^auth/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # Feeds
    url(r'^feeds/all', AllPosts()),

    # Editing
    url(r'^post/new$', AddPostView.as_view(), name='new_post'),
    url(r'^post/edit/(?P<pk>\d+)$', EditPostView.as_view(), name='edit_post'),
    url(r'^post/temp$', TempPostView.as_view(), name='temp_post'),

    url(r'^$', IndexView.as_view(), name='index'),

    # Old urls
    url(r'^(content|ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video|other)/(\d+)$', post_redirect),
    url(r'^users/([^/]+)/posts/(\d+)$', user_post),
]
