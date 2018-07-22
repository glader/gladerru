# coding: utf-8
# Проверяет <glader page=""> и <ItemLink> на правильность

import re
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from core.models import Item

for i in Item.objects.all():
    def tagsParser(result):
        if ' ' in result.group(1):
            _, tokens = result.group(1).split(' ', 1)  # noqa
        else:
            _, tokens = result.group(1), ""  # noqa
        params = dict((p, v) for p, v in re.findall('(\w+)=[\'\"]([^\'\"]+)[\'\"]', tokens))
        if 'item' in params:
            try:
                Item.objects.get(name=params['item'])
            except Item.DoesNotExist:
                print "Page '%s' not found in content '%s'" % (params['item'], i.name)

    def pageParser(result):
        try:
            Item.objects.get(name=result.group(1))
        except Item.DoesNotExist:
            print "Page '%s' not found in content '%s'" % (result.group(1), i.name)

    for text in (i.content, i.abstract):
        if text:
            re.sub('<:(.+?):>', tagsParser, text)
            re.sub('''<glader\s+page=['"]([^"']+)['"]>''', pageParser, text)
