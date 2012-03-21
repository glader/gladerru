# -*- coding: utf-8 -*-
# Перемещение портретов из отдельных элементов в поле image элементов

import re
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection
cursor = connection.cursor()

from core.models import Item, ItemType

t = ItemType.objects.get(name='PORTRAIT')
for p in Item.objects.filter(type=t):
    parent = p.get_parent()
    print parent.name,
    parent.image = p.image
    parent.save()
    print "ok"