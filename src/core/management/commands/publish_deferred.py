# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from random import choice

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from core.models import Post, Photo

import logging

AUTHORS = ['LAhmatyi', 'tinki', 'skyslayer', 'akafist', 'prophoter']

log = logging.getLogger('django.cron')


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        count = 0
        for item in Post.all.filter(status='deferred', date_created__lt=datetime.now()):

            log.info('Deferred publication for post %s (%s)', item.pk, item.get_absolute_url())
            if item.author.username == 'LAhmatyi':
                author = User.objects.get(username=choice(AUTHORS))
                item.author = author
                item.abstract = 'LAhmatyi'
                log.info('Author changed to %s for post %s (%s)', author.username, item.pk, item.get_absolute_url())

                for p in Photo.objects.filter(post=item):
                    p.author = author
                    p.save()

            item.status = 'pub'
            item.save()

            count += 1

        log.info('publish deferred: %s processed', count)
