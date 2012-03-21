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
from core.models import Item


def picture(result):
	p = Item.objects.get(image__contains=result.group(2))
	if 'float:right' in result.group(1):
		return '<div class="float_right"><glader pic="%s"></div>' % p.display_id()
	else:
		return '<glader pic="%s">' % p.display_id()


for i in Item.objects.filter(content__contains="/files/"):
	i.content = re.sub("files/other", "media/data/other", i.content)
	i.content = re.sub("files/images", "media/data/images", i.content)
	
	i.content = re.sub('(<a href="http://glader.ru/files/users/.+?/(\d+).JPG".+?</a>)', picture, i.content)

	i.save()
