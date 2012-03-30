# -*- coding: utf-8 -*-

import re
from itertools import groupby
import logging
import logging.handlers

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from core.forms import DiscountForm, FeedbackForm
from core.models import Redirect, Movie, Song, Rubric, Post, Word, Photo, Discount, Man, Mountain, Region, Studio, Skill, Tag
from core.templatetags.content import make_pages, link, get_mountains
from core.utils.common import clean_choice
from core.utils.search import search as search_provider
from core.views.common import render_to_response
from core.decorators import time_slow


@time_slow
def article(request, item_name):
    """ Статичные страницы """
    if Redirect.find(request.META['PATH_INFO']):
        return HttpResponsePermanentRedirect("http://%s%s" % (settings.DOMAIN, Redirect.find(request.META['PATH_INFO'])))

    # Добавить в редиректы
    try:
        rubric = Rubric.objects.get(name=item_name)
        return HttpResponsePermanentRedirect("http://%s%s" % (settings.DOMAIN, rubric.get_absolute_url()))
    except Rubric.DoesNotExist:
        pass

    article = get_object_or_404(Post, name=item_name)

    context = {'article': article}
    context.update(get_article_content(request, article))
    return render_to_response(request, 'article.html', context)


def get_article_content(request, item):
    if not (item.content and '<cut' in item.content):
        return {'content': item.content}

    pages = re.findall('<cut text="([^"]+)">(.+?)(?=<cut)', item.content, re.S)

    try:
        page = int(request.GET.get('page', 0))
    except ValueError:
        page = 0
    if page >= len(pages):
        page = 0

    menu = []
    content = ''
    i = 0
    for part in pages:
        menu.append(part[0])
        if i == page:
            content = part[1]
        i += 1

    return {'content': content,
            'menu': menu,
            'page': page,
            'previous': page > 0 and (page - 1, menu[page - 1]) or None,
            'next': page < len(menu) - 1 and (page + 1, menu[page + 1]) or None,
            }


def rubric(request, name):
    rubric = get_object_or_404(Rubric, name=name)
    context = {'rubric': rubric,
               'children': Rubric.objects.filter(parent=rubric),
               'articles': Post.objects.filter(rubric=rubric)
               }

    if rubric.template:
        template = 'special/%s' % rubric.template
    else:
        template = 'rubric.html'

    return render_to_response(request, template, context)


@time_slow
def mountains(request):
    context = get_mountains()
    context['YAMAPS_API_KEY'] = settings.YAMAPS_API_KEY
    return render_to_response(request, 'mountains.html', context)


@time_slow
def mountain(request, name):
    mountain = get_object_or_404(Mountain, name=name)
    return render_to_response(request, 'mountain.html', {'mountain': mountain})


def region(request, region_id):
    region = get_object_or_404(Region, pk=region_id)
    return render_to_response(request, 'mountains.html', get_mountains(region))

alphabet_letters = [[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'I', u'J', u'K', u'L', u'M', u'N', u'O', u'P', u'Q', u'R', u'S', u'T', u'U', u'V', u'W', u'X', u'Y', u'Z'],
                    [u'А', u'Б', u'В', u'Г', u'Д', u'Е', u'Ж', u'З', u'И', u'Й', u'К', u'Л', u'М', u'Н', u'О', u'П', u'Р', u'С', u'Т', u'У', u'Ф', u'Х', u'Ц', u'Ч', u'Ш', u'Щ', u'Ъ', u'Ы', u'Ь', u'Э', u'Ю', u'Я']]


def dictionary(request):
    filter = clean_choice(request.GET.get('filter'), [''] + [d[0] for d in Word.DICTIONARIES])
    words = Word.objects.all().order_by('title')
    if filter:
        words = words.filter(type=filter)

    present_letters = {}
    for word in words:
        present_letters.setdefault(word.title[0], []).append(word)
    return render_to_response(request, 'dictionary.html', {'filter': filter,
                                                           'alphabet_letters': alphabet_letters,
                                                           'present_letters': present_letters
                                                           })


def dictionary_word(request, name):
    word = get_object_or_404(Word, slug=name)
    return render_to_response(request, 'word.html', {'item': word})


def tricks(request):
    all_tricks = [t for t in Word.objects.all().order_by('type', 'title') if t.is_trick]
    cats = []
    for cat in Word.DICTIONARIES[2:]:
        cats.append((cat[0], cat[1], [t for t in all_tricks if t.type == cat[0]]))

    return render_to_response(request, 'tricks.html', {'cats': cats})


def trick(request, name):
    item = get_object_or_404(Word, slug=name)
    return render_to_response(request, 'trick.html', {'item': item})


def studies(request):
    studies = Studio.objects.all().order_by('title')
    return render_to_response(request, 'studies.html', {'studies': studies})


def studio(request, studio_name):
    studio = get_object_or_404(Studio, slug=studio_name)
    movies = Movie.objects.filter(studio=studio).order_by('-year', 'title')
    return render_to_response(request, 'studio.html', {'studio': studio, 'movies': movies})


@time_slow
def movies(request):
    context = {'page': request.GET.get('page', "2011")}
    year = context['page']

    movies = Movie.objects.all().order_by('-rating', 'title')
    if year == '06-00':
        movies = movies.filter(Q(year__lte='2006') | Q(year__isnull=True))
    elif re.match('^\d+$', year):
        movies = movies.filter(year=year)

    if not len(movies):
        movies = Movie.objects.all().order_by('-rating', 'title')

    return render_to_response(request, 'movies.html', {'movies': movies, 'year': year})


@time_slow
def movie(request, movie_name):
    movie = get_object_or_404(Movie, slug=movie_name)
    songs = Song.objects.filter(movie=movie)
    return render_to_response(request, 'movie.html', {'movie': movie, 'songs': songs, 'item': movie})


def teasers(request):
    movies = Movie.objects.filter(teaser__isnull=False).exclude(teaser='').order_by('-year', '-rating')
    return render_to_response(request, 'teasers.html', make_pages(movies, 10, request.GET.get('page', "")))


def soundtracks(request):
    movies = Movie.objects.filter(has_songs=True).order_by('-year', 'title')
    return render_to_response(request, 'soundtracks.html', make_pages(movies, 10, request.GET.get('page', "")))


def discounts(request):
    discounts = [(k, list(v)) for k, v in groupby(Discount.objects.all().order_by('city', 'card', 'discount'), lambda d: d.city)]
    return render_to_response(request, 'discounts.html', {'discounts': discounts})


def discount_new(request):
    if not request.user.is_authenticated():
        raise Http404

    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.user = request.user
            discount.save()
            return HttpResponseRedirect(reverse('discounts'))
    else:
        form = DiscountForm()

    return render_to_response(request, 'discount_form.html', {'form': form})


def discount_edit(request, discount_id):
    if not request.user.is_authenticated():
        raise Http404

    discount = get_object_or_404(Discount, pk=discount_id)
    if not (request.user == discount.user or request.user.get_profile().is_moderator):
        raise Http404

    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('discounts'))
    else:
        form = DiscountForm(instance=discount)

    return render_to_response(request, 'discount_form.html', {'form': form})


def discount_delete(request, discount_id):
    if not request.user.is_authenticated():
        raise Http404

    discount = get_object_or_404(Discount, pk=discount_id)
    if not (request.user == discount.user or request.user.get_profile().is_moderator):
        raise Http404

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        discount.delete()
        return HttpResponseRedirect(reverse('discounts'))

    return render_to_response(request, 'discount_delete.html', {'discount': discount})


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


def search(request):
    query = request.POST.get('query', '')

    log = logging.getLogger('django.search')
    log.info(u"%s\t%s", request.META['REMOTE_ADDR'], query)

    return render_to_response(request, 'search.html', {'result': search_provider(query),
                                                       'query': query
                                                       })


def feedback(request):
    if request.POST:
        context = {'form': FeedbackForm(request.POST)}
        if context['form'].is_valid():
            context['form'].send()
            context['message'] = u"Сообщение отправлено. Если вы указали обратный адрес, на него будет отправлен ответ."
    else:
        context = {'form': FeedbackForm(initial=request.GET)}

    return render_to_response(request, 'feedback.html', context)


def skills(request):
    blocks = [['icon_newbie.jpg', 8, 0],
              ['line_vertical_medium.jpg', 9, 4],
              ['line_arrow.jpg', 9, 6],

              ['icon_beginner.jpg', 8, 7],
              ['line_vertical.jpg', 9, 11],

              ['line_angle_left_down.jpg', 1, 12],
              ['line_horizontal_long.jpg', 2, 12],
              ['line_crossroad_left_right_down.jpg', 5, 12],
              ['line_horizontal_long.jpg', 6, 12],
              ['line_crossroad.jpg', 9, 12],
              ['line_horizontal_medium.jpg', 10, 12],
              ['line_horizontal_long.jpg', 12, 12],
              ['line_horizontal_medium.jpg', 15, 12],
              ['line_angle_right_down.jpg', 17, 12],
              ['line_arrow.jpg', 1, 13],
              ['line_arrow.jpg', 5, 13],
              ['line_arrow.jpg', 9, 13],
              ['line_arrow.jpg', 17, 13],

              ['icon_jibbing.jpg', 0, 14],
              ['line_vertical_medium.jpg', 1, 18],
              ['line_arrow.jpg', 1, 20],

              ['icon_carving.jpg', 4, 14],

              ['icon_freestyle.jpg', 8, 14],
              ['line_vertical.jpg', 9, 18],

              ['icon_freeride.jpg', 16, 14],
              ['line_vertical.jpg', 17, 18],


              ['line_angle_left_down.jpg', 5, 19],
              ['line_horizontal_long.jpg', 6, 19],
              ['line_crossroad.jpg', 9, 19],
              ['line_horizontal_medium.jpg', 10, 19],
              ['line_angle_right_down.jpg', 12, 19],
              ['line_arrow.jpg', 5, 20],
              ['line_arrow.jpg', 9, 20],
              ['line_arrow.jpg', 12, 20],

              ['line_angle_left_down.jpg', 14, 19],
              ['line_horizontal_medium.jpg', 15, 19],
              ['line_crossroad_left_down.jpg', 17, 19],
              ['line_arrow.jpg', 14, 20],
              ['line_arrow.jpg', 17, 20],

              ['icon_advanced_jibbing.jpg', 0, 21],
              ['icon_halfpipe_freestyle.jpg', 4, 21],
              ['icon_advanced_freestyle.jpg', 8, 21],
              ['icon_backcountry_freestyle.jpg', 12, 21],
              ['icon_advanced_freeride.jpg', 16, 21],


              ['icon_physical_culture.jpg', 16, 0],
              ['line_vertical_medium.jpg', 17, 4],
              ['line_arrow.jpg', 17, 6],
              ['icon_first_aid.jpg', 16, 7],

              ['icon_photo.jpg', 20, 0],
              ]

    skills = dict((s.slug, s) for s in Skill.objects.all())
    dop_blocks = []

    for block in blocks:
        block[1] *= 30
        block[2] *= 30
        code = block[0].replace('icon_', '').replace('.jpg', '')

        if code in skills:
            block.append(skills[code])
            dop_blocks.append(('text_%s.jpg' % code, block[1], block[2] + 90, skills[code]))

    return render_to_response(request, 'skills.html', {'blocks': blocks + dop_blocks,
                                                       'rubrics': Rubric.objects.all().order_by('title')})


def skill(request, name):
    skill = get_object_or_404(Skill, slug=name)
    context = {'skill': skill,
               'articles': Post.objects.filter(skill=skill).order_by('-date_created'),
               'tags': Tag.objects.filter(tag2skill__skill=skill).order_by('size')
               }
    return render_to_response(request, 'skill.html', context)
