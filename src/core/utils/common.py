# -*- coding: utf-8 -*-
from hashlib import md5

import cPickle as pickle

import re

from django.conf import settings
from django.core.cache import cache
from django.template import Context, loader
from django_glader_queue.models import Queue



translit = {u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e',
            u'ж': u'zh', u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k', u'л': u'l',
            u'м': u'm', u'н': u'n', u'о': u'o', u'п': u'p', u'р': u'r', u'с': u's',
            u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'x', u'ц': u'cz', u'ч': u'ch',
            u'ш': u'sh', u'щ': u'shh', u'ъ': u'_d', u'ы': u'_i', u'ь': u'_', u'э': u'ye',
            u'ю': u'yu', u'я': u'ya', u'ё': u'yo',
            u'æ': u'e',
            u'á': u'a', u'é': u'e', u'ć': u'c',
            u'ä': u'a', u'ü': u'u', u'ö': u'o',
            u'å': u'a', u'ů': u'u',
            u'č': u'c', u'š': u's', u'ř': u'r', u'ž': u'z',
            u'ø': u'o',
            }


def rus2translit(text):
    res = u''
    for c in text:
        if c in translit:
            res += translit[c]
        elif c.lower() in translit:
            res += translit[c.lower()].upper()
        else:
            res += c
    return res


def slug(title):
    return re.sub("\s", "", rus2translit(title.strip())).lower().replace('-', '')


def notice_admin(text, subject=u"Glader.ru: Ошибка на сайте"):
    for admin in settings.ADMINS:
        Queue.add_task('email', {'email': admin[1],
                                'subject': subject,
                                'content': "<html><body>%s</body></html>" % text})


def cached(cache_key='', timeout_seconds=1800):
    """Django cache decorator

    Example 1:
    class MenuItem(models.Model):
        @classmethod
        @cached('menu_root', 3600*24)
        def get_root(self):
            return MenuItem.objects.get(pk=1)

    Example 2:
    @cached(lambda u: 'user_privileges_%s' % u.username, 3600)
    def get_user_privileges(user):
        #...
    """
    def _cached(func):
        def do_cache(*args, **kwargs):
            if cache_key:
                if isinstance(cache_key, str):
                    key = cache_key % locals()
                elif callable(cache_key):
                    key = cache_key(*args, **kwargs)
            else:
                raw = [func.__name__, func.__module__, args, kwargs]
                pickled = pickle.dumps(raw, protocol=pickle.HIGHEST_PROTOCOL)
                key = md5(pickled).hexdigest()

            key = settings.CACHE_MIDDLEWARE_KEY_PREFIX + key
            data = cache.get(key)
            if data:
                return data
            data = func(*args, **kwargs)
            cache.set(key, data, timeout_seconds)
            return data
        return do_cache
    return _cached


def process_template(template, context):
    """ Обрабатывает шаблон, в котором первая строка считается заголовком """
    t = loader.get_template(template)
    c = Context(context)
    subject, content = t.render(c).split("\n", 1)
    return subject, content


def clean_choice(variant, variants):
    if variant in variants:
        return variant
    else:
        return variants[0]


