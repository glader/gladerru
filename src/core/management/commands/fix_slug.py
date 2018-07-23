# coding: utf-8
import re

from django.core.management.base import BaseCommand

from core.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):

        for post in Post.objects.all().order_by('-id'):
            s = post.slug
            slug = re.sub('[^a-zA-Z0-9-]', '', post.slug)
            slug = re.sub('\-+', '-', slug)
            if not post.in_index:
                slug = re.sub('\-+$', '', slug)

            post.slug = slug
            post.save()

            print s.encode('utf8'), slug
