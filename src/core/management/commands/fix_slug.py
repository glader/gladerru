# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.core.management.base import NoArgsCommand

from core.models import Post


class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        for post in Post.objects.all().order_by('-id'):
            s = post.slug
            slug = re.sub('[^a-zA-Z0-9-]', '', post.slug)
            slug = re.sub('\-+', '-', slug)
            if not post.in_index:
                slug = re.sub('\-+$', '', slug)

            post.slug = slug
            post.save()

            print s.encode('utf8'), slug
