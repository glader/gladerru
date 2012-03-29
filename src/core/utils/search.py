# -*- coding: utf-8 -*-
import urllib2
from cgi import escape
import re
from xml.etree import cElementTree as ET
import logging
import logging.handlers

from django.conf import settings

from core.models import Word, Movie, Man, Mountain, Tag, Post


def base_search(query):
    result = []
    for model in (Word, Movie, Man, Mountain, Tag):
        result.extend( model.objects.filter(title__icontains=query) )
    result.extend(Post.objects.filter(title__icontains=query, hidden=False).order_by('-date_created'))
    return result


def yandex_search(query):
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <request>
        <query>%s site:glader.ru</query>
        <page>0</page>
    </request>""" % escape(query.encode('utf8'))

    answer = urllib2.urlopen("http://xmlsearch.yandex.ru/xmlsearch?user=%s&key=%s" % (settings.YANDEX_XML_LOGIN, settings.YANDEX_XML_KEY), xml).read()

    log = logging.getLogger('search_raw')
    log.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(settings.LOGGING['handlers']['search']['filename'] + '_raw', maxBytes=1000000)
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
                page['snippet'] = "<br/>".join( [ re.sub('<[^>]+>', '', ET.tostring(passage).decode('utf8')).replace(u'&#1042;&#1099; &#1085;&#1077; &#1072;&#1074;&#1090;&#1086;&#1088;&#1080;&#1079;&#1086;&#1074;&#1072;&#1085;&#1099;!&#1042;&#1086;&#1081;&#1090;&#1080; &#1074; Glader.ru&#1047;&#1072;&#1088;&#1077;&#1075;&#1080;&#1089;&#1090;&#1088;&#1080;&#1088;&#1086;&#1074;&#1072;&#1090;&#1100;&#1089;&#1103; &#1089;&#1077;&#1081;&#1095;&#1072;&#1089;.', '')
                                                 for passage in group.find('doc').find('passages').findall('passage')]
                                                )

            result['pages'].append(page)

        return result

    else:
        return {}


def search(query):
    return {'base': base_search(query),
            'yandex': yandex_search(query)
            }