# -*- coding: utf-8 -*-
# Перемещение обложек фильмов из отдельных элементов в поле cover фильмов

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

t = ItemType.objects.get(name='MOVIE')
for movie in Item.objects.filter(type=t):
    for i in movie.get_children():
        if 'cover' in i.name:
            print movie.name,
            cursor.execute("UPDATE core_item SET cover=%s WHERE name=%s", ['data'+i.filename, movie.name])
            i.delete()
            print "ok"