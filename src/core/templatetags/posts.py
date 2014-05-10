# encoding: utf-8

from django.conf import settings
from django.template import Context, loader

from core.utils.common import cached


def render_to_string(template_name, context_dict=None):
    t = loader.get_template(template_name)
    return t.render(Context(context_dict or {}))


@cached(
    lambda post, mode='cut', user=None: "%srender/post/%s/%s" % (settings.CACHE_ROOT, post.id, mode or 'cut'),
    timeout_seconds=settings.CACHE_LONG_TIMEOUT,
)
def render_post_cached(post, mode='cut', user=None):
    """Формирование html кода поста. cut - вариант для ленты, full - для страницы поста"""
    return render_post(post, mode, user)


def render_post(post, mode='cut', user=None):
    return render_to_string('posts/%s_%s.html' % (post.type, mode), {'post': post, 'user': user, 'mode': 'normal'})
