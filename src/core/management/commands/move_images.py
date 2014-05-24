# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from django.core.management.base import NoArgsCommand

from core.models import Post, Photo
from core.utils.thumbnails import make_thumbnail, get_thumbnail_url


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for post in Post.objects.all():
            changed = False
            try:
                tree = BeautifulSoup(post.content, "html5lib")

                for tag in tree.find_all('a'):
                    href = tag.get('href')
                    if '/photos/' in href:
                        changed = True
                        print tag
                        photo = Photo.objects.get(pk=href.split('/')[-1])
                        tag['href'] = photo.yandex_fotki_image_src
                        tag['data-id'] = photo.id
                        tag['tagret'] = '_blank'

                        make_thumbnail(photo.yandex_fotki_image_src)
                        img = tree.new_tag("img", src=get_thumbnail_url(photo.yandex_fotki_image_src))
                        tag.img.replace_with(img)

                        print tag
                        print

                if changed:
                    post.content = tree.prettify()
                    post.save()

            except Exception, e:
                print e
