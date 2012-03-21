# -*- coding: utf-8 -*-
# Проверяет <glader page=""> и <ItemLink> на правильность

import re
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection
from core.models import Item, Tag

all_tags = {}

for i in Item.objects.filter(type=45):
    name = i.name[4:]
    t, _ = Tag.objects.get_or_create(name=name, title=i.title)
    all_tags[name] = t
    
for i in Item.objects.filter(type=51):
    name = i.name[9:]
    t, _ = Tag.objects.get_or_create(name=name, title=i.title, type=20)
    all_tags[name] = t
    
print "tags ready"

for i in Item.objects.all():
    i.tags.clear()
    categories = list(i.get_items('parents', 'CONCERN', 'POST_CATEGORY'))
    for c in categories:
        cat = all_tags[c.name[9:]]
        i.tags.add(cat)
    
    tags = list(i.get_items('parents', 'CONCERN', 'TAG'))
    for t in tags:
        cat = all_tags[t.name[4:]]
        i.tags.add(cat)
    
    i.rebuild_tags()

print "tags appropriated"

for t in Tag.objects.all():
    t.size = len(t.item_set.all())
    t.save()