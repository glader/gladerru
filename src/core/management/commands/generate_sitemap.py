# -*- coding: utf-8 -*-
import os

from django.test import Client
from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        c = Client()
        response = c.get('/dynamic_sitemap.xml')

        with open(os.path.join(settings.STATIC_ROOT, 'root', 'sitemap.xml'), 'w') as xml:
            xml.write(response.content)
