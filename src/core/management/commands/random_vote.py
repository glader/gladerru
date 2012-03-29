# -*- coding: utf-8 -*-
# раз в полчаса с вероятностью 1/5 голосует за случайный непроголосованный пост

from datetime import datetime, timedelta
from random import choice, randint

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User

from core.models import Post
from core.views.ugc import add_vote
import logging

BAD_AUTHORS = ['traektoria.boardshop']

log = logging.getLogger('django.cron')

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        curr = randint(2, 4)
        if curr != 4:
            log.info(u"Random value - %s", curr)
            return

        posts = list(Post.objects.filter(status='pub', date_created__gt=datetime.now() - timedelta(14), best__isnull=True)
                        .exclude(author__username__in=BAD_AUTHORS))

        if posts:
            log.info(u"Found posts %s", ", ".join('%s (%s)' % (post.get_absolute_url(), post.rating) for post in posts))

            post = choice(posts)
            user = User.objects.get(username='glader')
            add_vote(post, user, '127.0.0.1')

            log.info(u"Vote for post %s (%s)", post.id, post.get_absolute_url())

        else:
            log.info(u"no posts")