# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup

from django.core.management.base import NoArgsCommand

from core.models import Post


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for post in Post.objects.all().filter(pk=2980):
            if not post.content:
                continue

            soup = BeautifulSoup(post.content.encode('utf8'), from_encoding='utf8')
            for tag in soup.find_all('a'):
                href = tag.attrs.get('href', '')

                if not href.startswith('http'):
                    continue

                if 'img-fotki' in href or not post.used:
                    tag.attrs['rel'] = 'nofollow'

            content = soup.encode_contents(indent_level=2).decode('utf8')\
                .replace('<html><body>', '').replace('</body></html>', '')

            if content != post.content:
                post.content = content
                post.save()
                print "http://glader.ru" + post.get_absolute_url()
