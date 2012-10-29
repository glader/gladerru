# -*- coding: utf-8 -*-

from time import time
import functools

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from core.utils.log import get_logger
from core.templatetags.posts import render_post_cached, render_post
from core.views.common import render_to_response


def time_slow(f=None, logger=None, threshold=0.01):
    if not logger:
        logger = get_logger('slow_functions')

    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kw):
            if settings.DEBUG:
                start = time()
                try:
                    ret = f(*args, **kw)
                finally:
                    duration = time() - start
                    if duration > threshold:
                        logger.info('slow: %s %.9f seconds', f.__name__, duration)
                return ret
            else:
                return f(*args, **kw)
        return wrapper
    if f is not None:
        return decorated(f)
    return decorated


def auth_only(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("http://glader.ru/auth/login")
        return func(request, *args, **kwargs)
    return wrapper


def posts_feed(template="all.html"):
    u"""Оформление ленты постов. Оборачиваемая функция должна возвращать словарь с элементом 'items', сожержашем список постов"""
    def decorated(func):
        def wrapper(request, *args, **kwargs):
            context = func(request, *args, **kwargs)
            if isinstance(context, HttpResponse):
                return context

            render = render_post if request.user.is_authenticated() else render_post_cached
            context['posts'] = [render(post) for post in context['items']]
            return render_to_response(request, template, context)

        return wrapper
    return decorated
