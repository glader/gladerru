# coding: utf-8
import imghdr
import os
import urllib
from hashlib import md5
from io import StringIO

from PIL import Image
from django.conf import settings


def get_thumbnail_path(image_url):
    thumbnail_file = md5(image_url.encode('utf-8')).hexdigest()
    thumbnail_dir = thumbnail_file[0:2]
    return '%s/%s' % (thumbnail_dir, thumbnail_file)


def get_thumbnail_url(image_url):
    return settings.STATIC_URL + settings.THUMBNAIL_URL + get_thumbnail_path(image_url)


def make_thumbnail(image_url, force=False):
    thumbnail_path = get_thumbnail_path(image_url)
    full_path = os.path.join(settings.THUMBNAIL_ROOT, thumbnail_path)

    if os.path.exists(full_path) and not force:
        return False

    if not os.path.exists(os.path.dirname(full_path)):
        os.mkdir(os.path.dirname(full_path))

    content = StringIO(urllib.urlopen(image_url).read())
    content.seek(0)
    format = imghdr.what('', content.read(2048)) or 'jpeg'
    content.seek(0)

    im = Image.open(content)
    im.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)
    im.save(full_path, format=format)

    return True
