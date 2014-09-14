# -*- coding: utf-8 -*-
import simplejson

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, DetailView, ListView

from .models import Movie, Song, Man, Studio, Man2Movie, Photo
from .templatetags.movies import link
from .utils.common import slug


def render_to_string(request, template_name, context_dict={}):
    context = RequestContext(request, context_dict)
    t = loader.get_template(template_name)
    return t.render(context)


def render_to_response(request, template_name, context_dict={}, cookies={}):
    html = render_to_string(request, template_name, context_dict)
    response = HttpResponse(html)
    for k, v in cookies.items():
        response.set_cookie(k, v)
    return response


class StudioView(DetailView):
    model = Studio
    template_name = 'movies/studio.html'

    def get_context_data(self, **kwargs):
        context = super(StudioView, self).get_context_data(**kwargs)
        context['movies'] = Movie.objects.filter(studio=context['object']).order_by('-year', 'title')
        return context


class MoviesViews(ListView):
    template_name = 'movies/movies.html'

    def get_context_data(self, **kwargs):
        context = super(MoviesViews, self).get_context_data(**kwargs)
        context['year'] = self.kwargs['year']  # for submenu
        return context

    def get_queryset(self):
        year = self.kwargs['year']

        movies = Movie.objects.all().order_by('-rating', 'title')
        if year.isdigit():
            movies = movies.filter(year=year)

        if not len(movies):
            movies = Movie.objects.all().order_by('-rating', 'title')

        return movies


class MovieView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)
        context['songs'] = Song.objects.filter(movie=context['object'])
        context['item'] = context['object']
        context['page_identifier'] = context['object'].uid
        return context


class TeasersView(ListView):
    paginate_by = 10
    queryset = Movie.objects.filter(teaser__isnull=False).exclude(teaser='').order_by('-year', '-rating')
    template_name = 'movies/teasers.html'


class SoundtracksView(ListView):
    paginate_by = 10
    queryset = Movie.objects.filter(has_songs=True).order_by('-year', 'title')
    template_name = 'movies/soundtracks.html'


class PeopleView(TemplateView):
    template_name = 'movies/people.html'

    def get_context_data(self, **kwargs):
        riders = Man.interesting.all().order_by('title')
        present_letters = {}

        for r in riders:
            present_letters.setdefault(r.title[0], []).append(r)

        return {'alphabet_letters': settings.ALPHABET_LETTERS, 'present_letters': present_letters}


class ManView(DetailView):
    model = Man
    template_name = 'movies/rider.html'

    def render_to_response(self, context, **response_kwargs):
        if self.object.primary_synonim:
            return HttpResponsePermanentRedirect(self.object.primary_synonim.get_absolute_url())

        return super(ManView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        movies = Movie.objects.filter(man2movie__man=self.object, man2movie__role='actor').order_by('-year')
        photos = Photo.objects.filter(rider=self.object).order_by('-date_created')[:4]
        author_photos = Photo.objects.filter(photographer=self.object).order_by('-date_created')[:4]
        return {
            'item': self.object,
            'movies': movies,
            'photos': photos[:3],
            'more_photos': len(photos) > 3,
            'author_photos': author_photos[:3],
            'more_author_photos': len(author_photos) > 3,
        }


class ManPhotosView(ListView):
    man = None
    paginate_by = 20
    template_name = 'movies/rider_photos.html'

    def get_queryset(self):
        self.man = get_object_or_404(Man, slug=self.kwargs['slug'])
        return Photo.objects.filter(rider=self.man).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(ManPhotosView, self).get_context_data(**kwargs)
        context['title'] = mark_safe(
            u'%s - фотографии с %s участием' %
            (link(self.man), self.man.gender == 'm' and u'его' or u'её')
        )
        return context


class AuthorPhotosView(ListView):
    man = None
    paginate_by = 20
    template_name = 'movies/rider_photos.html'

    def get_queryset(self):
        self.man = get_object_or_404(Man, slug=self.kwargs['slug'])
        return Photo.objects.filter(photographer=self.man).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(AuthorPhotosView, self).get_context_data(**kwargs)
        context['title'] = mark_safe(
            u'%s - фотографии %s авторства' %
            (link(self.man), self.man.gender == 'm' and u'его' or u'её')
        )
        return context


class JsonResponse(HttpResponse):
    """ HttpResponse descendant, which return response with ``application/json`` mimetype. """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


# Admin

@permission_required('add_movie')
def create_rider(request):
    rider_titles = request.POST['rider']
    object_id = request.POST['object_id']
    movie = Movie.objects.get(pk=object_id)

    for rider_title in rider_titles.split(","):
        rider_name = slug(rider_title)
        try:
            rider = Man.objects.get(slug=rider_name)
            if rider.primary_synonim:
                rider = rider.primary_synonim

        except Man.DoesNotExist:
            rider = Man(slug=rider_name, title=rider_title, is_rider=True, hidden=True)
            rider.save()

        Man2Movie.objects.create(man=rider, movie=movie, role='actor')

    return HttpResponseRedirect('/admind/movies/movie/%d/' % movie.pk)


@permission_required('add_movie')
def create_teaser_announce(request):
    movie = Movie.objects.get(pk=request.GET.get('movie_pk'))

    Post = object()
    post = Post.objects.create(
        title=u'Тизер к фильму "%s"' % movie.title, content='',
        comment_count=0,
        status='pub',
        author=request.user,
        ip=request.META['REMOTE_ADDR'],
        type='teaser',
    )

    post.item = movie
    post.best = post.date_created
    post.save()

    return HttpResponseRedirect('/admind/movies/movie/%s/' % request.GET.get('movie_pk'))


@permission_required('add_movie')
def create_fullmovie_announce(request):
    movie = Movie.objects.get(pk=request.GET.get('movie_pk'))

    Post = object()
    post = Post.objects.create(
        title=u'Выложен фильм "%s"' % movie.title, content='',
        comment_count=0,
        status='pub',
        author=request.user,
        ip=request.META['REMOTE_ADDR'],
        type='full_movie',
    )

    post.item = movie
    post.best = post.date_created
    post.save()

    return HttpResponseRedirect('/admind/movies/movie/%s/' % request.GET.get('movie_pk'))


@permission_required('add_movie')
def create_tracklist_announce(request):
    movie = Movie.objects.get(pk=request.GET.get('movie_pk'))

    Post = object()
    post = Post.objects.create(
        title=u'Выложена музыка к фильму "%s"' % movie.title, content='',
        comment_count=0,
        status='pub',
        author=request.user,
        ip=request.META['REMOTE_ADDR'],
        type='soundtrack',
    )

    post.item = movie
    post.best = post.date_created
    post.save()

    return HttpResponseRedirect('/admind/movies/movie/%s/' % request.GET.get('movie_pk'))


# Redirects

def old_movie(request, movie_name):
    movie = get_object_or_404(Movie, slug=movie_name)
    return HttpResponsePermanentRedirect(movie.get_absolute_url())
