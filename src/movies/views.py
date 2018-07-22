# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Levenshtein import distance

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import View, TemplateView, DetailView, ListView

from core.decorators import class_view_decorator

from .models import Movie, Song, Man, Studio, Man2Movie, Photo
from .templatetags.movies import link
from .utils.common import slug


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

        movies = Movie.objects.all().order_by('title')
        if year.isdigit():
            movies = movies.filter(year=year)

        if not len(movies):
            movies = Movie.objects.all().order_by('title')

        return movies


class MovieView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)
        context['songs'] = Song.objects.filter(movie=context['object'])
        context['item'] = context['object']
        context['page_identifier'] = context['object'].uid
        context['movies'] = Movie.objects.filter(year=context['object'].year) \
            .exclude(pk=context['object'].pk).order_by('-pk')[:5]
        return context


class TeasersView(ListView):
    paginate_by = 10
    queryset = Movie.objects.filter(teaser__isnull=False).exclude(teaser='').order_by('-dt_teaser_added', '-year')
    template_name = 'movies/teasers.html'


class SoundtracksView(ListView):
    paginate_by = 10
    queryset = Movie.objects.filter(has_songs=True).order_by('-year', 'title')
    template_name = 'movies/soundtracks.html'


class PeopleView(TemplateView):
    template_name = 'movies/people.html'

    def get_context_data(self, **kwargs):
        riders = Man.interesting.filter(primary_synonim__isnull=True).order_by('title')
        present_letters = {}

        for r in riders:
            present_letters.setdefault(r.title[0], []).append(r)

        return {'alphabet_letters': settings.ALPHABET_LETTERS, 'present_letters': present_letters}


@class_view_decorator(permission_required('movies.can_edit_man'))
class CompareView(TemplateView):
    template_name = 'movies/compare.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['pairs'] = []

        man = list(Man.objects.filter(primary_synonim__isnull=True).order_by('id'))

        for m1 in man:
            for m2 in man:
                if m1.id >= m2.id:
                    continue

                dist = distance(m1.title, m2.title)
                if dist >= 4:
                    continue

                context['pairs'].append((m1, m2, dist))

        context['pairs'].sort(key=lambda pair: (pair[2], pair[0].title))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        man_from = Man.objects.get(pk=request.POST['from'])
        man_to = Man.objects.get(pk=request.POST['to'])

        man_from.primary_synonim = man_to
        man_from.save()
        return HttpResponseRedirect(reverse('people_compare'))


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
            '%s - фотографии с %s участием' %
            (link(self.man), self.man.gender == 'm' and 'его' or 'её')
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
            '%s - фотографии %s авторства' %
            (link(self.man), self.man.gender == 'm' and 'его' or 'её')
        )
        return context


class AddRidersView(View):
    def post(self, request, *args, **kwargs):
        rider_titles = request.POST['rider']
        object_id = request.POST['object_id']
        movie = Movie.objects.get(pk=object_id)

        for rider_title in rider_titles.split(","):
            rider_title = rider_title.strip()
            rider_name = slug(rider_title)
            try:
                rider = Man.objects.get(slug=rider_name)
                while rider.primary_synonim:
                    rider = rider.primary_synonim

            except Man.DoesNotExist:
                rider = Man.objects.create(slug=rider_name, title=rider_title, is_rider=True, hidden=True)

            Man2Movie.objects.create(man=rider, movie=movie, role='actor')

        return HttpResponseRedirect('/admind/movies/movie/%d/' % movie.pk)


class OldMovieRedirect(View):
    def dispatch(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, slug=kwargs['slug'])
        return HttpResponsePermanentRedirect(movie.get_absolute_url())
