# -*- coding: utf-8 -*-

import re
import logging

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from core.forms import FeedbackForm
from core.models import Redirect, Rubric, Post, Word, Skill, Tag
from core.utils.common import clean_choice
from core.utils.search import search as search_provider
from core.views.common import render_to_response
from core.decorators import time_slow


@time_slow
def article(request, item_name):
    """ Статичные страницы """
    if Redirect.find(request.META['PATH_INFO']):
        return HttpResponsePermanentRedirect("http://%s%s" % (settings.DOMAIN,
                                                              Redirect.find(request.META['PATH_INFO'])))

    # Добавить в редиректы
    try:
        rubric = Rubric.objects.get(name=item_name)
        return HttpResponsePermanentRedirect("http://%s%s" % (settings.DOMAIN, rubric.get_absolute_url()))
    except Rubric.DoesNotExist:
        pass

    article = get_object_or_404(Post, name=item_name)

    context = {
        'article': article,
        'page_identifier': 'post_%s' % article.id,
    }
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

alphabet_letters = [[u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split()],
                    [u'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.split()]]


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
    return render_to_response(request, 'trick.html', {'item': item, 'page_identifier': 'word_%s' % item.id})


def search(request):
    query = request.POST.get('query', '')

    if query:
        log = logging.getLogger('django.search')
        log.info(u"%s\t%s", request.META['REMOTE_ADDR'], query)
        context = {'result': search_provider(query), 'query': query}

    else:
        context = {'msg': u"Введите строку для поиска"}

    return render_to_response(request, 'search.html', context)


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
                                                       'rubrics': sorted(Rubric.objects.all(), key=lambda r: r.title)})


def skill(request, name):
    skill = get_object_or_404(Skill, slug=name)
    context = {'skill': skill,
               'articles': Post.objects.filter(skill=skill).order_by('-date_created'),
               'tags': Tag.objects.filter(tag2skill__skill=skill).order_by('size')
               }
    return render_to_response(request, 'skill.html', context)
