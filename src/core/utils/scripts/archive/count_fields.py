# -*- coding: utf-8 -*-
# Считает, какие поля встречаются у элементов определенного типа

import re
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection
from core.models import Item

fields = {}
skip_list = ('id', 'date_created', 'date_changed', 'title', 'content', 'name', 'type', 'item_type')

for p in Item.objects.all():
    type = p.type.name
    if type not in fields:
        fields[type] = {}

    for f in Item._meta.fields:
        if f.name not in skip_list and getattr(p, f.name) is not None \
            and getattr(p, f.name) != '' \
                and getattr(p, f.name) != 0:
                fields[type][f.name] = True


types = fields.keys()
types.sort()
for t in types:
    type_fields = fields[t].keys()
    type_fields.sort()
    print "            '" + t.lower() + "': ['" + "', '".join(type_fields) + "'],"
