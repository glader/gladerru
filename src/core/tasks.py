# -*- coding: utf-8 -*-
import logging
import functools

from celery import task

from core.models import Post, Tag

log = logging.getLogger('queue')


def log_task(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        log.info('Start task %s with args %r', func.__name__, args)
        func(*args, **kw)
        log.info('Finish task %s with args %r', func.__name__, args)

    return wrapper


@task()
@log_task
def check_celery(*args):
    log.info('Celery ok %r', args)


@task()
@log_task
def new_post_announces(post_id):
    u""" Добавить уведомление о посте в новости юзеров """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        log.error("Post announce: cannot find post with id %s", post_id)
        return

    # Теги поста
    for tag in post.tags.all():
        tag.recalc_posts()


@task()
@log_task
def tag_synonim(self, data):
    u"""Тегу назначен синоним, надо пересчитать все посты с этим тегом"""
    tag = Tag.objects.get(pk=data['tag_id'])

    items = tag.item_set.all()
    for i in items:
        i.tags.remove(tag)
        i.tags.add(tag.primary_synonim)
        i.rebuild_tags()
    items = tag.photo_set.all()
    for i in items:
        i.tags.remove(tag)
        i.tags.add(tag.primary_synonim)
        i.rebuild_tags()

    tag.primary_synonim.recalc_posts()
