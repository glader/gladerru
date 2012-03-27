# -*- coding: utf-8 -*-
from django.conf import settings
import django.dispatch
from django_queue.models import Queue
from django.core.cache import cache

from core.utils.common import process_template

new_comment_signal = django.dispatch.Signal()

def notice_about_comment(sender, **kwargs):
    current = sender.author
    if hasattr(kwargs['post'], 'author'):
        post_author = kwargs['post'].author
        if post_author and post_author != current and post_author.email:
            subject, content = process_template('email/new_post_comment.html', {
                                                        'post': kwargs['post'],
                                                        'comment': sender
                                                    })
            Queue.add_task('email', {'email': post_author.email,
                                     'subject': subject,
                                     'content': content})


        comment_author = kwargs['answer_on'].author
        if comment_author and comment_author != current and comment_author != post_author and comment_author.email:
            subject, content = process_template('email/new_comment_comment.html', {
                                                        'post': kwargs['post'],
                                                        'answer_on': kwargs['answer_on'],
                                                        'comment': sender
                                                    })
            Queue.add_task('email', {'email': comment_author.email,
                                     'subject': subject,
                                     'content': content})


def movie_rating(sender, **kwargs):
    if kwargs['post'].__class__.__name__ == 'Movie':
        kwargs['post'].rating += 0.1
        kwargs['post'].save()

def invalidate_comments_cache(sender, **kwargs):
    cache.delete(settings.CACHE_MIDDLEWARE_KEY_PREFIX + 'last_conversations')

new_comment_signal.connect(notice_about_comment)
new_comment_signal.connect(movie_rating)
new_comment_signal.connect(invalidate_comments_cache)
