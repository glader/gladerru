# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import md5
import cPickle as pickle
import re
import string

import bs4
from django.conf import settings
from django.core.cache import cache
from django.template import Context, loader
from django.core.mail import mail_admins, EmailMessage

translit = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l',
            'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
            'т': 't', 'у': '', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
            'ш': 'sh', 'щ': 'shh', 'ъ': '_d', 'ы': 'y', 'ь': 'y', 'э': 'ye',
            'ю': 'y', 'я': 'ya', 'ё': 'yo',
            'æ': 'e',
            'á': 'a', 'é': 'e', 'ć': 'c',
            'ä': 'a', 'ü': '', 'ö': 'o',
            'å': 'a', 'ů': '',
            'č': 'c', 'š': 's', 'ř': 'r', 'ž': 'z', 'ě': 'e',
            'ø': 'o',
            }


def rus2translit(text):
    res = ''
    for c in text:
        if c in translit:
            res += translit[c]
        elif c.lower() in translit:
            res += translit[c.lower()].upper()
        else:
            res += c
    return res


def slug(title):
    if not title:
        return ''

    return re.sub('[%s]+' % string.punctuation, '-', re.sub('\s+', '-', rus2translit(title.strip()))).lower()


def send_html_mail(subject, message, recipient_list):
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]
    message = EmailMessage(subject, message, to=recipient_list)
    message.content_subtype = 'html'
    message.send()


def notice_admin(text, subject='Glader.ru: Ошибка на сайте'):
    text = '<html><body>%s</body></html>' % text
    mail_admins(subject, text, html_message=text)


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
    subject, content = t.render(c).split('\n', 1)
    return subject, content


def clean_choice(variant, variants):
    if variant in variants:
        return variant
    else:
        return variants[0]


def count_text_len(html):
    tree = bs4.BeautifulSoup(html)
    strings = []
    for t in tree.find_all():
        for c in t.contents:
            if isinstance(c, bs4.element.NavigableString):
                strings.append(unicode(c).strip())

    return sum(map(len, strings))
