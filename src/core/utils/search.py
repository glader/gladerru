# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from xml.etree import cElementTree as ET
import logging
import logging.handlers
import re
import requests

from django.conf import settings

from core.models import Post
from mountains.models import Mountain
from movies.models import Movie, Studio, Man

CUTTED_TEXT = '&#1042;&#1099; &#1085;&#1077; &#1072;&#1074;&#1090;&#1086;&#1088;&#1080;&#1079;&#1086;&#1074;&#1072;' \
              '&#1085;&#1099;!&#1042;&#1086;&#1081;&#1090;&#1080; &#1074; Glader.ru&#1047;&#1072;&#1088;&#1077;&#1075;'\
              '&#1080;&#1089;&#1090;&#1088;&#1080;&#1088;&#1086;&#1074;&#1072;&#1090;&#1100;&#1089;&#1103; ' \
              '&#1089;&#1077;&#1081;&#1095;&#1072;&#1089;.'


def base_search(query):
    result = []
    for model in [Mountain, Movie, Studio, Man]:
        result.extend(model.objects.filter(title__icontains=query))

    result.extend(Post.objects.filter(title__icontains=query, hidden=False).order_by('-date_created'))
    return result


def yandex_search(query):
    answer = requests.get(
        'https://yandex.ru/search/xml',
        params={
            'user': settings.YANDEX_XML_LOGIN,
            'key': settings.YANDEX_XML_KEY,
            'query': '%s site:glader.r' % query,
            'page': 0,
        }
    ).content

    log = logging.getLogger('search_raw')
    log.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(settings.LOGGING['handlers']['search']['filename'] + '_raw',
                                                   maxBytes=1000000)
    log.addHandler(handler)
    log.info(answer)

    xml = ET.fromstring(answer)

    if xml.find('response').find('results'):
        result = {'found_human': xml.find('response').find('found-human').text,
                  'pages': [],
                  }

        for group in xml.find('response').find('results').find('grouping').findall('group'):
            page = {'url': group.find('doc').findtext('url'),
                    'title': re.sub('<[^>]+>', '', ET.tostring(group.find('doc').find('title')).decode('utf8')),
                    }
            if group.find('doc').find('passages'):
                page['snippet'] = '<br/>'.join(
                    [
                        re.sub('<[^>]+>', '', ET.tostring(passage).decode('utf8')).replace(CUTTED_TEXT, '')
                        for passage in group.find('doc').find('passages').findall('passage')
                    ]
                )

            result['pages'].append(page)

        return result

    else:
        return {}


def search(query):
    return {'base': base_search(query),
            'yandex': yandex_search(query)
            }
