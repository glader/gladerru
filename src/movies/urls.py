# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.views.generic import ListView, RedirectView
from django.contrib.auth.decorators import permission_required

from . import views
from .models import Studio

urlpatterns = patterns(
    '',
    url(r'^studies/(?P<slug>[^/]+)$', views.StudioView.as_view(), name='studio'),
    url(
        r'^studies/$',
        ListView.as_view(queryset=Studio.objects.all().order_by('title'), template_name='movies/studies.html'),
        name='studies',
    ),
    url(r'^movies/$', RedirectView.as_view(permanent=False, url='/movies/2014/'), name='movies'),
    url(r'^movies/teasers/$', views.TeasersView.as_view(), name='teasers'),
    url(r'^movies/soundtracks/$', views.SoundtracksView.as_view(), name='soundtracks'),
    url(r'^movies/(?P<year>[^/]+)/$', views.MoviesViews.as_view(), name='movies_by_year'),
    url(r'^movies/(?P<year>[^/]+)/(?P<slug>[^/]+)$', views.MovieView.as_view(), name='movie'),
    url(r'^people/(?P<slug>[^/]+)/photos$', views.ManPhotosView.as_view(), name='man_photos'),
    url(r'^people/(?P<slug>[^/]+)/author_photos$', views.AuthorPhotosView.as_view(), name='man_author_photos'),
    url(r'^people/(?P<slug>[^/]+)$', views.ManView.as_view(), name='man'),
    url(r'^people/$', views.PeopleView.as_view(), name='people'),

    # Create new elements
    url(r'^create/rider$', permission_required('add_movie')(views.AddRidersView.as_view()), name='create_rider'),

    # Old urls
    url(r'^movies/(?P<slug>[^/]+)$', views.OldMovieRedirect.as_view()),
)
