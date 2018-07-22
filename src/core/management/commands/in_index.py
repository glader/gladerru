# coding: utf-8
from xml.etree import cElementTree as ET

import requests
from django.core.management.base import NoArgsCommand

from core.models import Post


def get_longest(strings):
    strings = sorted(strings, key=len, reverse=True)
    return strings[0]


def get_position(query):
    data = b'''<?xml version="1.0" encoding="utf-8"?>
<request>
  <query>
    url:http://glader.ru%s
  </query>
  <groupings>
    <groupby attr="d" mode="deep" groups-on-page="10" docs-in-group="1" />
  </groupings>
</request>''' % query

    res = requests.post(
        'https://yandex.ru/search/xml',
        params={
            'user': 'glader',
            'key': '03.16500:4c105bcf94c33f2a66f57c564b3a1888',
            'sortby': 'rlv',
        },
        data=data
    )

    xml = ET.fromstring(res.content)

    for number, group in enumerate(xml.find('response').find('results').find('grouping').findall('group')):
        url = group.find('doc').findtext('url')
        if 'glader' in url:
            return number + 1

    return 1000


def search(query):
    try:
        position = get_position(query)
        return position
    except Exception:
        return None


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        prev = {int(l.split()[0].strip()) for l in open('index.log').readlines()}

        for post in Post.objects.filter(status='pub').order_by('-id'):
            if post.id in prev:
                continue

            url = post.get_absolute_url()

            print '-' * 40
            print post.id, url,

            pos = search(url)
            print pos

            open('index.log', 'a').write('%s\t%s\n' % (post.id, pos))
