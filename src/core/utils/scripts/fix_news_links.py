# -*- coding: utf-8 -*-
# Проверяет <glader page=""> и <ItemLink> на правильность

import re
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection
from core.models import News

for n in News.objects.all():
    n.content = re.sub(r'href="([^"]+)"', r'href="http://glader.ru\1"', n.content)
    n.save()
