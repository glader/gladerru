# encoding: utf-8
from __future__ import unicode_literals
import re
from urllib import quote

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.conf import settings

from core.models import Post, Photo, Tag, NewsCategory
from core.utils.thumbnails import get_thumbnail_url

from movies.models import Photo as ManPhoto

register = template.Library()


@register.simple_tag
def VK_API_ID():
    return settings.VK_API_ID


@register.inclusion_tag('block_top_menu.html')
def top_menu(level2='all_posts', level1=None):
    level2 = str(level2)
    categories = [
        [category.slug, category.get_absolute_url(), category.title, '']
        for category in NewsCategory.objects.all()
    ]
    submenu = {
        'posts': categories + [['new', '/post/new', 'написать', 'Предложить новость']],
        'articles': [
            ['newbie', '/skills/newbie', 'новичок', 'никогда не брал доску в руки'],
            ['beginner', '/skills/beginner', 'начинающий', 'умеешь спускаться елочкой'],
            ['freestyle', '/skills/freestyle', 'фристайл', 'те, кто хочет прыгать с трамплинов'],
            ['freeride', '/skills/freeride', 'фрирайд', 'тем, кто хочет катать в больших горах'],
            ['jibbing', '/skills/jibbing', 'джиббинг', 'тем, кто хочет слайдить по перилам'],
            ['carving', '/skills/carving', 'карвинг', 'тем, кто хочет резать дуги'],
            ['dictionary', '/terms/', 'словарь', 'Словарь всяких терминов'],
        ],
        'movies': [
            ['2014', '/movies/2014/', '2014', 'Фильмы 2014 года'],
            ['2013', '/movies/2013/', '2013', 'Фильмы 2013 года'],
            ['all', '/movies/all/', 'все', 'Все фильмы'],
            ['teasers', '/movies/teasers/', 'тизеры', 'Тизеры к фильмам'],
            ['soundtracks', '/movies/soundtracks/', 'саундтреки', 'Музыкальные треки к фильмам'],
            ['studies', '/studies/', 'студии', 'Авторы фильмов'],
            ['people', '/people/', 'райдеры', 'Участники съемок'],
        ],
        'mountains': [
            ['map', '/mountains', 'карта', 'Горки: информация, фотографии, цены, отзывы.'],
        ],
        'profile': [
            ['drafts', '/my/drafts', 'черновики', 'начатое и неоконченное'],
            ['settings', '/my/settings', 'настройки', ''],
        ]
    }

    def find_levels(level1, level2):
        if level1:
            return level1, level2

        if level2 in submenu:
            return level2, None

        for l1 in submenu.keys():
            for l2 in submenu[l1]:
                if l2[0] == level2:
                    return l1, level2

        return None, None

    level1, level2 = find_levels(level1, level2)
    return {'level1': level1, 'level2': level2, 'submen': level1 and submenu[level1] or []}


@register.filter
def decimal_cut(value, numbers=1):
    format = '%%0.%df' % numbers
    return format % value


@register.filter
def type_name(item):
    u"""Имя для иконки в поиске"""
    if isinstance(item, Post):
        if item.skill:
            return 'article'
        else:
            return 'post'
    return item.__class__.__name__.lower()

##########################################################


@register.filter
def linebreaks(text):
    if not text:
        return ''
    return re.sub('\r?\n', '<br/>\n', text)


@register.filter
def el(dic, key):
    return dic.get(key)


@register.filter
def link(item):
    if not item:
        return '[Отсутствует объект]'

    if isinstance(item, Tag):
        return mark_safe('<a href="%s" rel="tag">%s</a>' % (item.get_absolute_url(), item.title))

    if isinstance(item, User):
        return mark_safe('<a href="%s">%s</a>' % (item.get_absolute_url(), item.name))

    if isinstance(item, Photo) or isinstance(item, ManPhoto):
        return mark_safe('<a href="%s"><img class="userphoto" src="%s" alt="%s"></a>'
                         % (item.get_absolute_url(), thumbnail(item.yandex_fotki_image_src), item.title))

    return mark_safe('<a href="%s">%s</a>' % (item.get_absolute_url(), item.title))


@register.simple_tag
def post_edit_link(post, user):
    if post.can_edit(user):
        return mark_safe('(<a href="%s">ред.</a>)' % reverse('edit_post', args=[post.pk]))
    return ''


@register.simple_tag
def post_status(post):
    if post.status == 'save':
        return '(черновик)'
    if post.status == 'del':
        return '(удален)'
    if post.status == 'deferred':
        return '(будет опубликован %s)' % post.date_created
    return ''


@register.filter
def add_referrer(html, referrer):
    return re.sub(r'href="(http://[^"]+)"', r'href="\1#referrer=%s"' % referrer, html)


################################################################################
# Блоги

@register.inclusion_tag('block_pagination.html', takes_context=True)
def pagination(context, url=''):
    if not url:
        url = context['request'].get_full_path()

    # TODO: сделать с разбором query_string
    if 'start=' in url:
        url = re.sub('start=\d+&?', '', url)
        if url.endswith('?'):
            url = url[:-1]
    context['url'] = url
    return context


@register.inclusion_tag('block_post_panel.html')
def post_panel(post, user, mode='normal'):
    return {
        'post': post,
        'user': user,
        'mode': mode,
        'klass': post.__class__.__name__.lower(),
    }


@register.inclusion_tag('block_relative_posts.html')
def relative_posts(post):
    return {
        'relative_posts': Post.objects.filter(category=post.category).exclude(pk=post.pk).order_by('-date_created')[:4],
        'ab': 'table',
    }


@register.inclusion_tag('block_relative_posts.html')
def relative_articles(article):
    return {
        'relative_posts': Post.objects.filter(skill=article.skill).exclude(pk=article.pk)
                              .order_by('-date_created')[:4],
        'ab': 'table',
    }


@register.filter
def thumbnail(image_url):
    return get_thumbnail_url(image_url)


@register.filter
def is_extremebits(torrent):
    return 'extremebits' in torrent

##########################################################################################
# Admin site tags


@register.simple_tag
def get_admin_url(object):
    u"""Ссылка на редактирование эелмента"""
    return '/admind/%(app_label)s/%(module_name)s/%(object_id)s/' % {
        'app_label': object._meta.app_label,
        'module_name': object._meta.module_name,
        'object_id': quote(unicode(object.pk).encode('utf8'))
    }


@register.inclusion_tag('admin/tag_replace_form.html')
def admin_tag_replace(object_id):
    return {'tag': Tag.objects.get(pk=object_id),
            'object_id': object_id,
            }
