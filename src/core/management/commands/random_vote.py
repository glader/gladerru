# -*- coding: utf-8 -*-
# раз в полчаса с вероятностью 1/5 голосует за случайный непроголосованный пост

from datetime import datetime, timedelta
from random import choice, randint

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User

from core.models import Post
from core.views.ugc import add_vote

BAD_AUTHORS = ['traektoria.boardshop']

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        curr = randint(2, 4)
        if curr != 4:
            open(settings.CRON_LOG_PATH, "a").write("%s\t%s\n" % (datetime.now(), curr))
            return

        posts = list(Post.objects.filter(status='pub', date_created__gt=datetime.now() - timedelta(14), best__isnull=True)
                        .exclude(author__username__in=BAD_AUTHORS))

        if posts:
            open(settings.CRON_LOG_PATH, "a").write("%s\tfound posts %s\n" % (datetime.now(), ", ".join('%s (%s)' % (post.get_absolute_url(), post.rating) for post in posts)))

            post = choice(posts)
            user = User.objects.get(username='glader')
            add_vote(post, user, '127.0.0.1')

            open(settings.CRON_LOG_PATH, "a").write("%s\tvote for post %s (%s)\n" % (datetime.now(), post.id, post.get_absolute_url()))

        else:
             open(settings.CRON_LOG_PATH, "a").write("%s\tno posts\n" % datetime.now())