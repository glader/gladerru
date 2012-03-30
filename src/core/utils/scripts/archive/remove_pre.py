# -*- coding: utf-8 -*-

import re
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection

from core.models import Item, ItemType

for p in Item.objects.all():
    if p.content:
        p.content = re.sub("<:(End)?Pre:>", "", p.content)
        p.save()
