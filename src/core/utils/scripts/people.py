# -*- coding: utf-8 -*-
# Отчеты в посты

import re
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from core.models import Man

people = Man.objects.all()
for m in people:
    m.save()