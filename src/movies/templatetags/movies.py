# encoding: utf-8
import re

from django import template
from django.utils.safestring import mark_safe
from django.core.paginator import QuerySetPaginator
from django.conf import settings

from ..models import Movie, Man, Song

register = template.Library()


def make_pages(queryset, items_at_page=20, current_page=None):
    pages = QuerySetPaginator(queryset, items_at_page)

    page_number = validate_page_number(current_page, pages.num_pages)
    posts = pages.page(page_number).object_list
    context = {'items': posts}

    context.update(other_pages(page_number, pages.num_pages))
    return context


def validate_page_number(page, total):
    if page:
        try:
            page = int(page)
            if 1 <= page <= total:
                return page
        except ValueError:
            pass

    return 1


def other_pages(page, total):
    return {
        'pages': range(1, total + 1),
        'showed_pages': [p for p in range(1, total + 1) if abs(p - page) <= 4],
        'page_number': page,
        'first_page': page != 1 and 1 or None,
        'prev_page': page != 1 and page - 1 or None,
        'next_page': page != total and page + 1 or None,
        'last_page': page != total and total or None,
    }


@register.filter
def link(item):
    if not item:
        return u"[Отсутствует объект]"

    return mark_safe(u'<a href="%s">%s</a>' % (item.get_absolute_url(), item.title))


@register.inclusion_tag('block_riders.html')
def riders(movie):
    riders = Man.objects.filter(man2movie__movie=movie, man2movie__role='actor').order_by('title')
    return {'riders': riders}


@register.inclusion_tag('movies/block_soundtrack_list.html')
def soundtrack(movie):
    return {'songs': Song.objects.filter(movie=movie)}


@register.inclusion_tag('movies/block_soundtrack_list.html')
def soundtrack_list(songs):
    return {'songs': songs, 'SOUNDTRACKS_PREFIX': settings.SOUNDTRACKS_PREFIX}


@register.inclusion_tag('movies/block_recent_teasers.html')
def recent_teasers():
    return {'movies': Movie.objects.filter(dt_teaser_added__isnull=False).order_by('-dt_teaser_added')[:2]}


@register.inclusion_tag('movies/block_recent_movies.html')
def recent_movies():
    return {'movies': Movie.objects.filter(dt_fullmovie_added__isnull=False).order_by('-dt_fullmovie_added')[:2]}


@register.filter
def set_video_width(teaser, new_width=500):
    try:
        width = re.search('width="(\d+)"', teaser).group(1)
        height = re.search('height="(\d+)"', teaser).group(1)

        new_height = int(float(new_width) * int(height) / int(width))
        teaser = re.sub('width="(\d+)"', 'width="%s"' % new_width, teaser)
        teaser = re.sub('height="(\d+)"', 'height="%s"' % new_height, teaser)
    except Exception:
        pass

    return teaser
