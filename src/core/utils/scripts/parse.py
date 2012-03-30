# encoding: cp1251

import re
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection
cursor = connection.cursor()

from core.models import Item, ItemType


def lat(title):
	import md5
	return md5.new(title.encode('cp1251')).hexdigest()


i = 0
for l in open('geo').readlines():
	if i == 0:
		data = [0, 0, 0, None]
		if l[:3] != 'var':
			raise Exception(l)

		res = re.search("GLatLng\(([\d\.]+), ([\d\.]+)\)", l)
		data[0] = res.group(1)
		data[1] = res.group(2)

	if i == 1:
		res = re.search('title:"([^"]+)"', l)
		data[2] = res.group(1)

	if i == 3:
		res = re.search('<a href=([^>]+)>Сайт курорта</a>', l)
		if res:
			data[3] = res.group(1)

	i += 1
	if i == 7:
		title = data[2].decode('cp1251')
		try:
			m = Item.objects.get(title=title, type=ItemType.by_name['MOUNTAIN'])
			print "exist"
		except Item.DoesNotExist:
			name = lat(title)
			m = Item(name=name, type=ItemType.by_name['MOUNTAIN'], title=title)
			print "new"

		m.latitude = data[0]
		m.longitude = data[1]
		m.url = m.url or data[3]
		m.save()

		#print data, ","
		i = 0
