# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.core.management.base import NoArgsCommand

from core.views.ugc import add_to_yaphoto


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        d = '.\\data'

        with open('images', 'r') as l:
            log = l.read()

        from os.path import join
        for root, dirs, files in os.walk(d):
            for file in files:
                path = join(root, file)
                print path,

                if path.encode('utf8') in log:
                    print 'ready'
                    continue

                _, url = add_to_yaphoto(open(path, 'rb'))
                print url

                with open('images', 'a') as l:
                    l.write('%s\t%s\n' % (path.encode('utf8'), url))
