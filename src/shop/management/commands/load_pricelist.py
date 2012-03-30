# -*- coding: utf-8 -*-
import os
import urllib
from lxml import etree
import re
from datetime import datetime

from django.core.management.base import NoArgsCommand
from django.conf import settings
#from core.utils.common import get_logger

from shop.models import Category, Brand, Item

URL = 'http://www.dosok.net/vkontakte-xml.php'


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        #log = get_logger('shop_load')
        #log.info('Start loading')

        pricelist = self.get_pricelist()

        tree = etree.fromstring(pricelist)

        for item_el in tree.findall('goods/item'):
            item_dict = self.get_item(item_el)

            try:
                item = Item.objects.get(pk=item_dict['id'])
                for field in 'image title size sex description price url'.split():
                    setattr(item, field, item_dict[field])
                item.update = datetime.now()
                item.save()

            except Item.DoesNotExist:
                item_dict['category'] = self.get_category(item_dict)
                if not item_dict['category']:
                    continue

                item_dict['brand'] = self.get_brand(item_dict['brand'])
                item_dict['update'] = datetime.now()
                del item_dict['podcategory']

                Item.objects.create(**item_dict)

    def get_pricelist(self):
        #pricelist = urllib.urlopen(URL).read()
        path = os.path.dirname(__file__)
        return open(os.path.join(path, 'sample.xml')).read()

    def get_item(self, item_el):
        result = {}
        for field in 'image title size sex description price url brand category podcategory'.split():
            result[field] = item_el.find(field).text
        match = re.search('info(\d+)', result['url'])
        result['id'] = int(match.group(1))

        return result

    def get_category(self, item_dict):
        if not item_dict['category'] or not item_dict['podcategory']:
            return

        try:
            category = Category.objects.get(title=item_dict['category'])
        except Category.DoesNotExist:
            category = Category.objects.create(title=item_dict['category'])

        if item_dict['podcategory']:
            try:
                subcategory = Category.objects.get(title=item_dict['podcategory'])
            except Category.DoesNotExist:
                subcategory = Category.objects.create(title=item_dict['podcategory'], parent=category)

            return subcategory

        else:
            return category

    def get_brand(self, brand_title):
        try:
            return Brand.objects.get(title=brand_title)
        except Brand.DoesNotExist:
            return Brand.objects.create(title=brand_title)
