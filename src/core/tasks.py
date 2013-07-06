# -*- coding: utf-8 -*-
import logging
import functools

from celery import task
from django.contrib.auth.models import User

from core.models import News, UserNews, Movie, Friend, Post, Tag

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


def post_announce(post, announce_type, tag=None):
    params = {
        'user_url': post.author.get_absolute_url(),
        'username': post.author.first_name,
        'post_url': post.get_absolute_url(),
        'post_title': post.title,
    }

    if tag:
        params['tag_url'] = tag.get_absolute_url()
        params['tag_title'] = tag.title

    return News.objects.create(type=announce_type, content=News.messages[announce_type] % params, item=post)


@task()
@log_task
def new_post_announces(post_id):
    u""" Добавить уведомление о посте в новости юзеров """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        log.error("Post announce: cannot find post with id %s", post_id)
        return

    news = post_announce(post, 'new_post')

    # Друзьям автора
    for friend in Friend.objects.filter(user_b=post.author):
        UserNews.objects.create(user=friend.user_a, news=news)

    # Теги поста
    for tag in post.tags.all():
        tag.recalc_posts()


@task()
@log_task
def best_post_announces(post_id):
    u"""Добавить уведомление о посте в новости юзеров"""
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        log.error("Post announce: cannot find post with id %s", post_id)
        return

    news = post_announce(post, 'good_post')
    for user in User.objects.all():
        if user == post.author:
            continue
        UserNews.objects.create(user=user, news=news)


@task()
@log_task
def new_teaser(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    params = {
        'movie_url': movie.get_absolute_url(),
        'movie_title': movie.title,
    }
    news = News.objects.create(type='new_teaser', content=News.messages['new_teaser'] % params, item=movie)

    for user in User.objects.all():
        UserNews.objects.create(user=user, news=news)


@task()
@log_task
def new_fullmovie(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    params = {
        'movie_url': movie.get_absolute_url(),
        'movie_title': movie.title,
    }
    news = News.objects.create(type='new_fullmovie', content=News.messages['new_fullmovie'] % params, item=movie)

    for user in User.objects.all():
        UserNews.objects.create(user=user, news=news)


@task()
@log_task
def new_tracklist(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    params = {
        'movie_url': movie.get_absolute_url(),
        'movie_title': movie.title,
    }
    news = News.objects.create(type='new_tracklist', content=News.messages['new_tracklist'] % params, item=movie)

    for user in User.objects.all():
        UserNews.objects.create(user=user, news=news)


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
