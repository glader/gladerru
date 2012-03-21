# -*- coding: utf-8 -*-

import re
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection

from core.models import Item, ItemType

type = ItemType.objects.get(name='USERPHOTO')
for p in Item.objects.filter(type=type):
    if p.filename:
        p.filename = re.sub('^files/', '', p.filename)
        p.save()
    else:
        print p.name, "field is empty"
    
