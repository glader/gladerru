# -*- coding: utf-8 -*-
from itertools import chain

from django.core.management.base import NoArgsCommand
from django.core.mail import mail_admins

from core.models import Photo, Man, Movie
from core.utils.thumbnails import make_thumbnail

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        count = 0
        total = 0

        images = [
            (photo.yandex_fotki_image_src for photo in Photo.objects.filter(yandex_fotki_image_src__isnull=False)),
            (man.image for man in Man.objects.filter(image__isnull=False)),
            (movie.cover for movie in Movie.objects.filter(cover__isnull=False)),
        ]

        for image_url in chain(*images):
            try:
                count += make_thumbnail(str(image_url))
                total += 1

            except IOError, e:
                print e

        mail_admins('Glader.ru: thumbnails', "%s/%s thumbnails processed" % (count, total))