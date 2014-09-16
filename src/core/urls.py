# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views.content import *
from views.ugc import *
from feeds import *
from django.contrib.auth.views import password_reset

urlpatterns = patterns(
    '',
    url(r'^content/(?P<pk>[^/]+)\.htm$', ArticleView.as_view(), name='article'),
    url(r'^rubric/(?P<name>[^/]+)$', RubricView.as_view(), name='rubric'),

    url(r'^(?P<slug>ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video)$', CategoryView.as_view(),
        name='category'),
    url(r'^(ekipirovka|gory|obzory|obuchenie|sorevnovaniya|foto|video)/(\d+)$', post_view, name='post'),

    url(r'^terms/(?P<slug>[^/]+)$', DictionaryWordView.as_view(), name='dictionary_word'),
    url(r'^terms/', DictionaryView.as_view(), name='dictionary'),
    url(r'^skills/(?P<slug>[^/]+)$', SkillView.as_view(), name='skill'),
    url(r'^skills/$', SkillsView.as_view(), name='skills'),
    url(r'^tricks/(?P<slug>[^/]+)$', TrickView.as_view(), name='trick'),
    url(r'^tricks/$', TricksView.as_view(), name='tricks'),
    url(r'^search', SearchView.as_view(), name='search'),
    url(r'^feedback', FeedbackView.as_view(), name='feedback'),

    url(r'^auth/login$', login, name='login'),
    url(r'^auth/registration$', registration, name='registration'),
    url(r'^auth/logout$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^auth/reset$', password_reset, name='password_reset'),
    url(r'^auth/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^auth/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^auth/reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    # Feeds
    (r'^feeds/all', AllPosts()),

    # Editing
    url(r'^post/new$', AddPostView.as_view(), name='new_post'),
    url(r'^post/edit/(?P<pk>\d+)$', EditPostView.as_view(), name='edit_post'),
    url(r'^post/temp$', TempPostView.as_view(), name='temp_post'),

    url(r'^$', IndexView.as_view(), name='index'),

    # Old urls
    url(r'^users/([^/]+)/posts/(\d+)$', user_post),
)
