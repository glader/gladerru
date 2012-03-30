# -*- coding: utf-8 -*-

import re
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection

from core.models import Item, ItemType


def thumbnail(result):
    url = result.group(1)
    if not 'thumbnails' in url:
        return url

    print "found thumbnail", url,

    res = re.search('/files_users_([^/]+)_(\d+)\.jpg', url)
    if res:
        name = 'files/users/' + res.group(1) + '/' + res.group(2) + '.jpg'
        print name,
        pic = Item.objects.get(filename=name)
        print pic.get_thumbnail_url()
        return pic.get_thumbnail_url()

    else:
        print "BAD URL"
        exit(0)

for i in Item.objects.filter(content__isnull=False):
    i.content = re.sub('(http[^\s]+\.jpg)', thumbnail, i.content)
    i.save()
