# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bs4
import requests
from xml.etree import cElementTree as ET


from django.core.management.base import NoArgsCommand

from core.models import Post


def get_longest(strings):
    strings = sorted(strings, key=len, reverse=True)
    return strings[0]


def get_position(query):
    data = b'''<?xml version="1.0" encoding="utf-8"?>
<request>
  <query>
    "%s"
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
    positions = []
    for w in xrange(15, 30):
        q = b' '.join(query.encode('utf8').replace(b'"', b'\\"').split(b' ')[:w])
        position = 1000
        for _ in xrange(3):
            try:
                position = get_position(q)
                break
            except Exception:
                print '.'

        print w, position
        if position <= 10:
            positions.append(position)

    if positions:
        return float(sum(positions)) / len(positions)
    else:
        return 1000


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        prev = {int(l.split()[0].strip()) for l in open('pos.log').readlines()}

        for post in Post.objects.filter(status='pub').order_by('-id'):
            if not post.content:
                continue

            if post.id in prev:
                continue

            tree = bs4.BeautifulSoup(post.content.encode('utf8'), from_encoding='utf8')

            strings = []
            for t in tree.find_all():
                for c in t.contents:
                    if isinstance(c, bs4.element.NavigableString):
                        strings.append(unicode(c).strip())

            string = get_longest(strings)
            if not len(string):
                continue

            s = string.encode('utf8')

            open('test', 'a').write(b'%s: %s\n' % (post.id, s))

            print '-' * 40
            print post.id

            avg_position = search(string)

            open('pos.log', 'a').write('%s\t%0.2f\n' % (post.id, avg_position))
