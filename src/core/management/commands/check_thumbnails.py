# -*- coding: utf-8 -*-
from itertools import chain

from django.core.management.base import NoArgsCommand

from core.models import Photo
from movies.models import Man, Movie
from mountains.models import Mountain, MountainPhoto
from core.utils.thumbnails import make_thumbnail
import logging

log = logging.getLogger('django.cron')


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        count = 0
        total = 0

        images = [
            (photo.yandex_fotki_image_src for photo in Photo.objects.filter(yandex_fotki_image_src__isnull=False)),
            (man.image for man in Man.objects.filter(image__isnull=False)),
            (movie.cover for movie in Movie.objects.filter(cover__isnull=False)),
            (mountain.image for mountain in Mountain.objects.filter(image__isnull=False)),
            (mp.image for mp in MountainPhoto.objects.filter(image__isnull=False)),
        ]

        for image_url in chain(*images):
            try:
                count += make_thumbnail(str(image_url))
                total += 1

            except IOError, e:
                print e

        log.info(u"%s/%s thumbnails processed", count, total)
