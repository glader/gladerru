# coding: utf-8
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.contrib.auth.models import User

from core.models import Post, Movie, Tag, Man2Movie, ItemVote
import logging

settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '../../templates/3'), )

log = logging.getLogger('django.cron')


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()

        # FIXME: переписать это дело на один запрос
        print 'posts'
        i = 0
        for p in Post.objects.all():
            cursor.execute('SELECT SUM(vote) FROM core_itemvote WHERE object_id=%s and content_type_id=52', [p.id])
            p.rating = cursor.fetchone()[0] or 0

            comments = p.comments.all().order_by('-date_created')
            if len(comments) > 0:
                p.comment_count = len(comments)
                p.last_comment_date = comments[0].date_created
            else:
                p.comment_count = 0
                p.last_comment_date = None

            p.rebuild_tags()
            print i, chr(13),
            i += 1

        print 'movies'
        i = 0
        for m in Movie.objects.all():
            cursor.execute('SELECT SUM(vote) FROM core_itemvote WHERE object_id=%s and content_type_id=37', [m.id])
            m.rating = int(cursor.fetchone()[0] or 0)
            if m.content:
                m.rating += 0.5
            if m.teaser:
                m.rating += 1
            if m.torrent:
                m.rating += 2
            if m.full_movie:
                m.rating += 5
            if Man2Movie.objects.filter(movie=m).count():
                m.rating += 0.5

            comments = m.comments.all()
            if len(comments) > 0:
                m.comment_count = len(comments)
                m.last_comment_date = comments[0].date_created
            else:
                m.comment_count = 0
                m.last_comment_date = None

            m.rating += 0.1 * len(comments)
            m.save()
            print i, chr(13),
            i += 1

        print 'tags'
        i = 0
        for t in Tag.objects.all():
            t.size = t.post_set.all().count() + t.photo_set.all().count()
            t.recalc_posts()
            t.save()
            print i, chr(13),
            i += 1

        print 'users'
        for u in User.objects.all():
            profile = u.get_profile()
            profile.calculate()

            rating = profile.pub_post_count * 0.1 + profile.pic_count * 0.05 + profile.comment_count * 0.01
            for post in Post.objects.filter(author=u, status='pub'):
                rating += post.rating * 0.1
            rating += ItemVote.objects.filter(user=u).count() * 0.01
            profile.rating = rating
            profile.save()

        log.info('recalc')
