# -*- coding: utf-8 -*-

import re
import logging

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, FormView
from django.conf import settings

from core.forms import FeedbackForm
from core.models import Post, Word, Skill
from core.utils.common import clean_choice
from core.utils.search import search as search_provider


class ArticleView(TemplateView):
    template_name = 'core/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['article'] = get_object_or_404(Post, slug=kwargs['pk'])
        context['page_identifier'] = 'post_%s' % context['article'].id
        context.update(self.get_article_content(context['article']))
        return context

    def get_article_content(self, item):
        if not (item.content and '<cut' in item.content):
            return {'content': item.content}

        pages = re.findall('<cut text="([^"]+)">(.+?)(?=<cut)', item.content, re.S)

        try:
            page = int(self.request.GET.get('page', 0))
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


class DictionaryView(TemplateView):
    template_name = 'core/dictionary.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryView, self).get_context_data(**kwargs)
        context['filter'] = clean_choice(self.request.GET.get('filter'), [''] + [d[0] for d in Word.DICTIONARIES])
        words = Word.objects.all().order_by('title')
        if context['filter']:
            words = words.filter(type=context['filter'])

        context['alphabet_letters'] = settings.ALPHABET_LETTERS
        context['present_letters'] = {}
        for word in words:
            context['present_letters'].setdefault(word.title[0], []).append(word)
        return context


class DictionaryWordView(DetailView):
    template_name = 'core/word.html'
    queryset = Word.objects.all()


class TricksView(TemplateView):
    template_name = 'core/tricks.html'

    def get_context_data(self, **kwargs):
        context = super(TricksView, self).get_context_data(**kwargs)
        all_tricks = [t for t in Word.objects.all().order_by('type', 'title') if t.is_trick]
        context['cats'] = []
        for cat in Word.DICTIONARIES[2:]:
            context['cats'].append((cat[0], cat[1], [t for t in all_tricks if t.type == cat[0]]))
        return context


class TrickView(DetailView):
    template_name = 'core/trick.html'
    queryset = Word.objects.all()


class SearchView(TemplateView):
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        query = self.request.POST.get('query', '')
        if query:
            log = logging.getLogger('django.search')
            log.info(u"%s\t%s", request.META['REMOTE_ADDR'], query)
            context = {'result': search_provider(query), 'query': query}
        else:
            context = {'msg': u"Введите строку для поиска"}

        return self.render_to_response(context)


class FeedbackView(FormView):
    template_name = 'core/feedback.html'
    form_class = FeedbackForm
    success_url = '/feedback/?save=ok'

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        context['saved'] = bool(self.request.GET.get('save'))
        return context

    def form_valid(self, form):
        form.send()


class SkillsView(TemplateView):
    template_name = 'core/skills.html'

    def get(self, request, *args, **kwargs):
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

        return self.render_to_response({'blocks': blocks + dop_blocks})


class SkillView(TemplateView):
    template_name = 'core/skill.html'

    def get_context_data(self, **kwargs):
        context = super(SkillView, self).get_context_data(**kwargs)
        context['skill'] = get_object_or_404(Skill, slug=kwargs['slug'])
        context['articles'] = Post.objects.filter(skill=context['skill']).order_by('-date_created')
        return context
