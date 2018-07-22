# coding: utf-8
import re
from django.core.management.base import NoArgsCommand
from django.conf import settings
from xml.etree import ElementTree as ET
import httplib
import mimetypes
import requests

from core.models import Post
from bs4 import BeautifulSoup


class Command(NoArgsCommand):
    def get_image(self, post):
        tree = BeautifulSoup(post.content.encode('utf8'), from_encoding='utf8')
        try:
            for a in tree.find_all('a'):
                if 'img-fotki.yandex.ru' in a['href']:
                    return re.sub('#.+$', '', a['href'])

            for img in tree.find_all('img'):
                if img['src'].startswith('http'):
                    return img['src']

        except IndexError:
            pass

    def handle_noargs(self, **options):
        for post in Post.objects.filter(type='post'):
            try:
                if not post.icon:
                    img = self.get_image(post)
                    if img:
                        if 'fotki' not in img:
                            print post.id, "upload", img,
                            _, img = add_to_yaphoto(requests.get(img).content)
                            print img
                        post.icon = img
                        post.save()
            except Exception as e:
                print e


def force_str(s, encoding='utf-8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    return str(s)

# FIXME: не ascii-имена файлов вообще-то требуется кодировать в quoted-printable


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        if isinstance(value, unicode):
            L.append('Content-Type: text/plain; charset=utf-8')
        L.append('')
        L.append(force_str(value))
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def post_multipart(host, port, selector, fields, files, headers=None):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host, port)
    all_headers = {
        'Content-Type': content_type
    }
    if headers:
        all_headers.update(headers)
    h.request('POST', selector, body, all_headers)
    res = h.getresponse()
    return res.status, res.reason, res.read()


def add_to_yaphoto(content):

    files = [('image', 'image', content), ]
    status, reason, result = post_multipart(
        settings.YAFOTKI_STORAGE_OPTIONS['host'],
        None,
        settings.YAFOTKI_STORAGE_OPTIONS['post'],
        {},
        files,
        headers={'Authorization': 'OAuth %s' % settings.YAFOTKI_STORAGE_OPTIONS['token']}
    )

    if status != 201:
        raise ValueError("Cannot upload image: %s %s %s (host %s)" %
                         (status, reason, result, settings.YAFOTKI_STORAGE_OPTIONS['host']))

    tree = ET.fromstring(result)
    try:
        id = tree.find('.//{http://www.w3.org/2005/Atom}id').text
        url = tree.find('.//{http://www.w3.org/2005/Atom}content').attrib['src']
        return id, url

    except TypeError:
        raise ValueError('Bad info answer: %s' % result)
