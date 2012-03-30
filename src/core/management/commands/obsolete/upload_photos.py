# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management.base import NoArgsCommand

from core.models import Photo
from core.views.ugc import add_to_yaphoto


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for photo in Photo.objects.filter(image__isnull=False, yandex_fotki_image_id__isnull=True).order_by('pk'):
            print "PHOTO", photo.id, photo.image
            id, url = add_to_yaphoto(open(os.path.join(settings.THUMBNAIL_ROOT, photo.image.path), 'rb'))
            photo.yandex_fotki_image_id = id
            photo.yandex_fotki_image_src = url

            photo.make_thumbnail()
