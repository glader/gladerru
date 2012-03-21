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
teaser_type = ItemType.objects.get(name='TEASER_LINK')
for teaser in Item.objects.filter(type=teaser_type):
    movie = teaser.get_parent() 
    if movie.type.name == 'MOVIE':
        movie.youtube = (movie.youtube or '') + (teaser.youtube or '') + (teaser.rutube or '')
        teaser.delete()
        movie.save()
    else:
        print "Not movie", movie.name
        
            
print "ok"
