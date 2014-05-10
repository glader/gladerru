# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views import *


urlpatterns = patterns('',
    url(r'^studies/([^/]+)$', studio, name='studio'),
    url(r'^studies/$', studies, name='studies'),
    url(r'^movies/teasers/$', teasers, name='teasers'),
    url(r'^movies/soundtracks/$', soundtracks, name='soundtracks'),
    url(r'^movies/(?P<year>[^/]+)/$', movies_by_year, name='movies_by_year'),
    url(r'^movies/(?P<year>[^/]+)/(?P<name>[^/]+)$', movie, name='movie'),
    url(r'^movies/$', movies, name='movies'),
    url(r'^people/([^/]+)/photos$', man_photos, name='man_photos'),
    url(r'^people/([^/]+)/author_photos$', man_author_photos, name='man_author_photos'),
    url(r'^people/([^/]+)$', man, name='man'),
    url(r'^people/$', people, name='people'),
    url(r'^ajax/picturebox', picturebox),

    # Create new elements
    url(r'^create/rider$', create_rider, name='create_rider'),
    url(r'^create/teaser_announce$', create_teaser_announce, name='create_teaser_announce'),
    url(r'^create/fullmovie_announce$', create_fullmovie_announce, name='create_fullmovie_announce'),
    url(r'^create/tracklist_announce$', create_tracklist_announce, name='create_tracklist_announce'),

    # Old urls
    url(r'^movies/([^/]+)$', old_movie),
)
