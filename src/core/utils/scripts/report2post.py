# -*- coding: utf-8 -*-
# Отчеты в посты

import re
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection
from core.models import Item, Tag, ItemType

reports = Item.objects.get(name='reports').get_children()
for r in reports:
    type = ItemType.by_name['POST']
    name = Item.get_next_name('POST')
    post = Item(name=name, type=type,
                title=r.title, content=r.content,
                comment_count=0, status='pub',

                )
    post.save()
    author = Item.objects.get(pk=1)
    post.add_rel(author, 'parents', 'AUTHOR')
    post.tags.add(*Tag.process_tags(u'Разное, Отчет'))
    post.date_created = r.date_created
    post.save()
    print post.get_absolute_url()
