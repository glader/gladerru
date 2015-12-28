# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup

from django.core.management.base import NoArgsCommand

from core.models import Post
from movies.models import Movie, Studio
from mountains.models import Mountain


def process(content, used=False):
    if not content:
        return

    soup = BeautifulSoup(content.encode('utf8'), from_encoding='utf8')
    for tag in soup.find_all('a'):
        href = tag.attrs.get('href', '')

        if not href.startswith('http'):
            continue

        if 'img-fotki' in href or not used:
            tag.attrs['rel'] = 'nofollow'

    content = soup.encode_contents(indent_level=2).decode('utf8')\
        .replace('<html><body>', '').replace('</body></html>', '')

    return content


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for post in Post.objects.all():
            content = process(post.content, post.used)

            if content and content != post.content:
                post.content = content
                post.save()
                print "http://glader.ru" + post.get_absolute_url()

        for movie in Movie.objects.all():
            content = process(movie.content)

            if content and content != movie.content:
                movie.content = content
                movie.save()
                print "http://glader.ru" + movie.get_absolute_url()

        for studio in Studio.objects.all():
            content = process(studio.content)

            if content and content != studio.content:
                studio.content = content
                studio.save()
                print "http://glader.ru" + studio.get_absolute_url()

        for mountain in Mountain.objects.all():
            content = process(mountain.content)

            if content and content != mountain.content:
                mountain.content = content
                mountain.save()
                print "http://glader.ru" + mountain.get_absolute_url()
