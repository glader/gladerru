# -*- coding: utf-8 -*-

from time import time
import functools

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import Context, loader

from core.utils.log import get_logger
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
    u"""Оформление ленты постов. Оборачиваемая функция должна возвращать словарь с элементом 'items',
    содержащем список постов
    """
    def decorated(func):
        def wrapper(request, *args, **kwargs):
            context = func(request, *args, **kwargs)
            if isinstance(context, HttpResponse):
                return context

            context['posts'] = [render_to_string('core/post_cut.html', {'post': post, 'user': None, 'mode': 'normal'})
                                for post in context['posts']]
            return render_to_response(request, template, context)
        return wrapper
    return decorated


def render_to_string(template_name, context_dict=None):
    t = loader.get_template(template_name)
    return t.render(Context(context_dict or {}))


from django.utils.decorators import method_decorator


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator
