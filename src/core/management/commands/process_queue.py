# -*- coding: utf-8 -*-
import logging
import logging.handlers

from django.core.management.base import NoArgsCommand
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User

from django_queue.models import Queue

from core.models import News, UserNews, Movie, Friend, Post, Tag

class Command(NoArgsCommand):
    def send_email(self, data):
        message = EmailMessage(data['subject'].strip(),
                               data['content'],
                               'Glader.ru <robot@glader.ru>',
                               [data['email']],
                               )
        message.content_subtype = "html"
        message.send()

    def post_announce(self, post, announce_type, tag=None):
        params = {'user_url': post.author.get_absolute_url(),
                  'username': post.author.first_name,
                  'post_url': post.get_absolute_url(),
                  'post_title': post.title
                  }
        if tag:
            params['tag_url'] = tag.get_absolute_url()
            params['tag_title'] = tag.title

        news = News.objects.create(type=announce_type, content=News.messages[announce_type] % params, item=post)
        return news

    def new_post(self, data):
        u""" Добавить уведомление о посте в новости юзеров """
        post = Post.objects.get(pk=data['post_id'])
        news = self.post_announce(post, 'new_post')

        # Друзьям автора
        for friend in Friend.objects.filter(user_b=post.author):
            UserNews.objects.create(user=friend.user_a, news=news)

        # Теги поста
        for tag in post.tags.all():
            tag.recalc_posts()


    def best_post(self, data):
        u"""Добавить уведомление о посте в новости юзеров"""
        if not data['klass'] == 'Post':
            # Пока ничего не делаем с голосованиями за картинки и фильмы
            return

        post = Post.objects.get(pk=data['post_id'])
        news = self.post_announce(post, 'good_post')
        for user in User.objects.all():
            if user == post.author:
                continue
            UserNews.objects.create(user=user, news=news)


    def new_friend(self, data):
        u"""Уведомление юзерам что их друг нашел нового друга"""
        user = User.objects.get(pk=data['user'])
        new_friend = User.objects.get(pk=data['new_friend'])
        params = {'user_url': user.get_absolute_url(),
                  'username': user.first_name,
                  'friend_url': new_friend.get_absolute_url(),
                  'friend_title': new_friend.first_name
                  }
        message = News.messages['new_friend'] % params
        news = News.objects.create(type='new_friend', content=message, item=new_friend)

        for friend in Friend.objects.filter(user_b=user):
            if friend.user_a == new_friend:
                continue

            UserNews.objects.create(user=friend.user_a, news=news)


    def new_teaser(self, data):
        movie = Movie.objects.get(pk=data['movie_id'])
        params = {'movie_url': movie.get_absolute_url(),
                  'movie_title': movie.title,
                  }
        news = News.objects.create(type='new_teaser', content=News.messages['new_teaser'] % params, item=movie)

        for user in User.objects.all():
            UserNews.objects.create(user=user, news=news)


    def new_fullmovie(self, data):
        movie = Movie.objects.get(pk=data['movie_id'])
        params = {'movie_url': movie.get_absolute_url(),
                  'movie_title': movie.title,
                  }
        news = News.objects.create(type='new_fullmovie', content=News.messages['new_fullmovie'] % params, item=movie)

        for user in User.objects.all():
            UserNews.objects.create(user=user, news=news)


    def new_tracklist(self, data):
        movie = Movie.objects.get(pk=data['movie_id'])
        params = {'movie_url': movie.get_absolute_url(),
                  'movie_title': movie.title,
                  }
        news = News.objects.create(type='new_tracklist', content=News.messages['new_tracklist'] % params, item=movie)

        for user in User.objects.all():
            UserNews.objects.create(user=user, news=news)


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


    def handle_noargs(self, **options):
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(settings.QUEUE_LOG_PATH, maxBytes=1000000)
        LOG_FORMAT = u'%(levelname)s %(asctime)s: %(message)s'
        LOG_TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
        handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT))
        log.addHandler(handler)
        log.info('Start work')

        handlers = {'email': self.send_email,
                    'best_post': self.best_post,
                    'new_post': self.new_post,
                    'new_friend': self.new_friend,
                    'new_teaser': self.new_teaser,
                    'new_fullmovie': self.new_fullmovie,
                    'new_tracklist': self.new_tracklist,
                    'tag_synonim': self.tag_synonim,
                    }

        for task in Queue.get_tasks():
            log.info('Task %s - start' % task.id)
            log.info("%s: %s" % (task.id, task.data))
            task.start_work()
            try:
                handlers[task.task](task.data)
                task.finish()
                log.info('Task %s - finish' % task.id)

            except Exception, e:
                task.error(unicode(e))
                log.info('Task %s - error' % task.id)

        Queue.flush()
        log.info('Finish work')
