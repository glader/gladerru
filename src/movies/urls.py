# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^studies/([^/]+)$', views.studio, name='studio'),
    url(r'^studies/$', views.studies, name='studies'),
    url(r'^movies/teasers/$', views.teasers, name='teasers'),
    url(r'^movies/soundtracks/$', views.soundtracks, name='soundtracks'),
    url(r'^movies/(?P<year>[^/]+)/$', views.movies_by_year, name='movies_by_year'),
    url(r'^movies/(?P<year>[^/]+)/(?P<name>[^/]+)$', views.movie, name='movie'),
    url(r'^movies/$', views.movies, name='movies'),
    url(r'^people/([^/]+)/photos$', views.man_photos, name='man_photos'),
    url(r'^people/([^/]+)/author_photos$', views.man_author_photos, name='man_author_photos'),
    url(r'^people/([^/]+)$', views.man, name='man'),
    url(r'^people/$', views.people, name='people'),
    url(r'^ajax/picturebox', views.picturebox),

    # Create new elements
    url(r'^create/rider$', views.create_rider, name='create_rider'),
    url(r'^create/teaser_announce$', views.create_teaser_announce, name='create_teaser_announce'),
    url(r'^create/fullmovie_announce$', views.create_fullmovie_announce, name='create_fullmovie_announce'),
    url(r'^create/tracklist_announce$', views.create_tracklist_announce, name='create_tracklist_announce'),

    # Old urls
    url(r'^movies/([^/]+)$', views.old_movie),
)
