# -*- coding: utf-8 -*-
from datetime import datetime
from random import choice

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User

from django_queue.models import Queue

from core.models import Post, Photo

AUTHORS = ['LAhmatyi', 'tinki', 'skyslayer', 'akafist', 'prophoter']

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        count = 0
        for item in Post.all.filter(status='deferred', date_created__lt=datetime.now()):

            open(settings.CRON_LOG_PATH, "a").write("%s\tDeferred publication for post %s (%s)\n" % (datetime.now(), item.pk, item.get_absolute_url()))
            if item.author.username == 'LAhmatyi':
                author = User.objects.get(username=choice(AUTHORS))
                item.author = author
                item.abstract = 'LAhmatyi'
                open(settings.CRON_LOG_PATH, "a").write("%s\tAuthor changed to %s for post %s (%s)\n" % (datetime.now(), author.username, item.pk, item.get_absolute_url()))

                for p in Photo.objects.filter(post=item):
                    p.author = author
                    p.save()

            item.status = 'pub'
            item.save()

            Queue.add_task('new_post', {"post_id":item.id})

            count += 1

        open(settings.CRON_LOG_PATH, "a").write("%s\tpublish deferred: %s\n" % (datetime.now(), count))