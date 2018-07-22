# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import os
from itertools import chain

from django.core.management.base import NoArgsCommand

from core.models import Post, Photo, Word
from core.utils.thumbnails import make_thumbnail, get_thumbnail_url


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        replaces = dict(
            line.strip().split('\t')
            for line in open(os.path.join(os.path.dirname(__file__), '..', '..', 'migrations', 'images.dat'))
            .readlines()
        )

        for post in chain(Post.objects.all(), Word.objects.all()):
            changed = False
            try:
                tree = BeautifulSoup(post.content, "html5lib")

                for tag in tree.find_all('a'):
                    href = tag.get('href')
                    if not href:
                        continue

                    if ('/photos/' in href and '/users/' in href) or ('/pic/' in href and '.glader.ru' in href):
                        changed = True
                        print tag
                        photo = Photo.objects.get(pk=href.split('/')[-1])
                        tag['href'] = photo.yandex_fotki_image_src
                        tag['data-id'] = photo.id
                        tag['target'] = '_blank'

                        make_thumbnail(photo.yandex_fotki_image_src)
                        img = tree.new_tag("img", src=get_thumbnail_url(photo.yandex_fotki_image_src))
                        if tag.img:
                            tag.img.replace_with(img)

                        print tag

                for tag in tree.find_all('img'):
                    image = tag.get('src')
                    for replace in replaces.keys():
                        if image and replace in image:
                            print tag['src'], '->', replaces[replace]
                            tag['src'] = replaces[replace]
                            changed = True

                if changed:
                    post.content = str(tree)
                    post.save()

            except Exception, e:
                raise
                print e
