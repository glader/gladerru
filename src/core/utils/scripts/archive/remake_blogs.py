# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from django.db import connection

from core.models import Item, ItemType

from pprint import pprint

os.system("mysql -uroot --database=gladerru < gladerru.sql")

# Новые категории
cats = ([u'Фристайл', 'freestyle'],
        [u'Фрирайд',  'freeride'],
        [u'Джибинг',  'jibbing'],
        [u'Карвинг',  'carving'],
        [u'Снаряга',  'equipment'],
        [u'События',  'events'],
        [u'Фильмы',  'movies'],
        [u'Я новичок',  'newbie'],
        [u'Разное', 'other'],
        )
cat_items = {}

type = ItemType(name='POST_CATEGORY', description=u"Категория постов")
type.save()
i = 1
for c in cats:
    category = Item(type=type, name='category_' + c[1], title=c[0], abstract=c[1], order=i)
    category.save()
    cat_items[c[1]] = category
    i += 1

# перенос постов в категории
old_blogs = {'blog_123': 'equipment',
             'blog_contests': 'events',
             'blog_equipment': 'equipment',
             'blog_Exotic': 'equipment',
             'blog_gismo': 'newbie',
             'blog_lma': 'equipment',
             'blog_movie': 'movies',
             }

post_type = ItemType.objects.get(name__in=['POST'])
for p in Item.objects.filter(type__in=[post_type]):
    parent = p.get_parent()
    category = None
    if parent and parent.type.name == 'BLOG':
        if parent.name in old_blogs:
            category = cat_items[old_blogs[parent.name]]

    if not category:
        category = cat_items['other']

    p.add_rel(category, 'parents', 'CONCERN')

    # Удаляем связи с блогами
    p.del_rel(rel_direction='parents', rel_name='BELONGS')


# Удаление старых блогов
