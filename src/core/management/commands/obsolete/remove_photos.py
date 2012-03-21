# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management.base import NoArgsCommand

from core.models import Photo
from core.views.ugc import add_to_yaphoto
from urllib2 import Request, urlopen
from xml.etree import ElementTree as ET
import httplib
import re

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for i, photo in enumerate(Photo.objects.filter(yandex_fotki_image_id__isnull=False).order_by('pk')):
            print i, chr(13),
            try:
                urlopen(photo.yandex_fotki_image_src).read()
                if photo.image:
                    path = os.path.join(settings.MEDIA_ROOT, photo.image.path)
                    if os.path.exists(path):
                        #sh = open('/home/www/projects/gladerru/drop.sh', 'a')
                        sh = open('drop.sh', 'a')
                        sh.write('rm %s\n' % path)
                        sh.close()
                        
                        photo.image = None
                        photo.save()
                    else:
                        print "No image %s (%s)" % (photo.id, path)

            except Exception, e:
                print "Cannot download photo %s (%s) (%s)" % (photo.id, photo.yandex_fotki_image_src, e)
