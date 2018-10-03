# coding: utf-8
import logging
from itertools import chain

from django.core.management.base import BaseCommand

from core.models import Photo as CorePhoto
from core.utils.thumbnails import make_thumbnail
from mountains.models import Mountain, MountainPhoto
from movies.models import Man, Movie, Photo

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        count = 0
        total = 0

        images = [
            (photo.yandex_fotki_image_src for photo in CorePhoto.objects.filter(yandex_fotki_image_src__isnull=False)),
            (man.image for man in Man.objects.filter(image__isnull=False)),
            (movie.cover for movie in Movie.objects.filter(cover__isnull=False)),
            (photo.yandex_fotki_image_src for photo in Photo.objects.filter(yandex_fotki_image_src__isnull=False)),
            (mountain.image for mountain in Mountain.objects.filter(image__isnull=False)),
            (mp.image for mp in MountainPhoto.objects.filter(image__isnull=False)),
        ]

        for image in chain(*images):
            image_url = str(image)
            if not image_url:
                continue

            try:
                count += make_thumbnail(str(image_url))
                total += 1

            except IOError as e:
                print(e)

        log.info('%s/%s thumbnails processed', count, total)
