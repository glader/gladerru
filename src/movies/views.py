# -*- coding: utf-8 -*-
import simplejson

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.template import RequestContext, loader

from .models import Movie, Song, Man, Studio, Man2Movie, Photo, PictureBox
from .templatetags.movies import make_pages, link
from .utils.common import slug


alphabet_letters = [[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'I', u'J', u'K', u'L', u'M', u'N', u'O', u'P', u'Q', u'R', u'S', u'T', u'U', u'V', u'W', u'X', u'Y', u'Z'],
                    [u'А', u'Б', u'В', u'Г', u'Д', u'Е', u'Ж', u'З', u'И', u'Й', u'К', u'Л', u'М', u'Н', u'О', u'П', u'Р', u'С', u'Т', u'У', u'Ф', u'Х', u'Ц', u'Ч', u'Ш', u'Щ', u'Ъ', u'Ы', u'Ь', u'Э', u'Ю', u'Я']]


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


def studies(request):
    studies = Studio.objects.all().order_by('title')
    return render_to_response(request, 'studies.html', {'studies': studies})


def studio(request, studio_name):
    studio = get_object_or_404(Studio, slug=studio_name)
    movies = Movie.objects.filter(studio=studio).order_by('-year', 'title')
    return render_to_response(request, 'studio.html', {'studio': studio, 'movies': movies})


def movies(request):
    context = {'page': "2013"}
    year = context['page']

    movies = Movie.objects.all().order_by('-rating', 'title')
    if year.isdigit():
        movies = movies.filter(year=year)

    if not len(movies):
        movies = Movie.objects.all().order_by('-rating', 'title')

    return render_to_response(request, 'movies.html', {'movies': movies, 'year': year})


def movies_by_year(request, year):
    context = {'page': year}
    year = context['page']

    movies = Movie.objects.all().order_by('-rating', 'title')
    if year.isdigit():
        movies = movies.filter(year=year)

    if not len(movies):
        movies = Movie.objects.all().order_by('-rating', 'title')

    return render_to_response(request, 'movies.html', {'movies': movies, 'year': year})


def movie(request, year, name):
    movie = get_object_or_404(Movie, slug=name)
    songs = Song.objects.filter(movie=movie)
    return render_to_response(request, 'movie.html', {'movie': movie, 'songs': songs, 'item': movie, 'page_identifier': 'movie_%s' % movie.id})


def teasers(request):
    movies = Movie.objects.filter(teaser__isnull=False).exclude(teaser='').order_by('-year', '-rating')
    return render_to_response(request, 'teasers.html', make_pages(movies, 10, request.GET.get('page', "")))


def soundtracks(request):
    movies = Movie.objects.filter(has_songs=True).order_by('-year', 'title')
    return render_to_response(request, 'soundtracks.html', make_pages(movies, 10, request.GET.get('page', "")))


def people(request):
    riders = Man.interesting.all().order_by('title')
    present_letters = {}
    for r in riders:
        present_letters.setdefault(r.title[0], []).append(r)
    content = {'alphabet_letters': alphabet_letters, 'present_letters': present_letters}
    return render_to_response(request, 'people.html', content)


def man(request, man_name):
    item = get_object_or_404(Man, slug=man_name)
    if item.primary_synonim:
        return HttpResponsePermanentRedirect(item.primary_synonim.get_absolute_url())
    movies = Movie.objects.filter(man2movie__man=item, man2movie__role='actor').order_by('-year')
    photos = Photo.objects.filter(rider=item).order_by('-date_created')[:4]
    author_photos = Photo.objects.filter(photographer=item).order_by('-date_created')[:4]
    return render_to_response(request, 'rider.html', {'item': item,
                                                      'movies': movies,
                                                      'photos': photos[:3],
                                                      'more_photos': len(photos) > 3,
                                                      'author_photos': author_photos[:3],
                                                      'more_author_photos': len(author_photos) > 3,
                                                      })


def man_photos(request, slug):
    item = get_object_or_404(Man, slug=slug)
    context = make_pages(Photo.objects.filter(rider=item).order_by('-date_created'), current_page=request.GET.get('page', ""))
    context['title'] = mark_safe(u'%s - фотографии с %s участием' % (link(item), item.gender == 'm' and u'его' or u'её'))
    return render_to_response(request, 'rider_photos.html', context)


def man_author_photos(request, slug):
    item = get_object_or_404(Man, slug=slug)
    context = make_pages(Photo.objects.filter(photographer=item).order_by('-date_created'), current_page=request.GET.get('page', ""))
    context['title'] = mark_safe(u'%s - фотографии %s авторства' % (link(item), item.gender == 'm' and u'его' or u'её'))
    return render_to_response(request, 'rider_photos.html', context)


class JsonResponse(HttpResponse):
    """ HttpResponse descendant, which return response with ``application/json`` mimetype. """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


def picturebox(request):
    picture = get_object_or_404(Photo, pk=request.GET.get('picture_id'))
    user = request.user.is_authenticated() and request.user or None
    record = PictureBox(user=user, picture=picture, action=request.GET.get('action'))
    record.save()
    if request.GET.get('action') == 'good':
        result = {}
    else:
        next_picture = PictureBox.get_next_picture(user)
        result = {'success': True, 'picture_id': next_picture.pk, 'preview': link(next_picture)}
    return JsonResponse(result)


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

    return HttpResponseRedirect('/admind/core/movie/%d/' % movie.pk)


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

    return HttpResponseRedirect('/admind/core/movie/%s/' % request.GET.get('movie_pk'))


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

    return HttpResponseRedirect('/admind/core/movie/%s/' % request.GET.get('movie_pk'))


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

    return HttpResponseRedirect('/admind/core/movie/%s/' % request.GET.get('movie_pk'))


# Redirects

def old_movie(request, movie_name):
    movie = get_object_or_404(Movie, slug=movie_name)
    return HttpResponsePermanentRedirect(movie.get_absolute_url())
