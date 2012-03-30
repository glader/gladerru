# -*- coding: utf-8 -*-
from itertools import chain

from django.core.management.base import NoArgsCommand

from core.models import Movie, Man, Studio, Word, Mountain, Keyword


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        Keyword.objects.filter(type='auto').delete()

        for item in chain(Movie.objects.all(), Man.objects.all(), Studio.objects.all(),
                          Word.objects.all(), Mountain.objects.all()):
            Keyword.objects.create(keyword=item.title, url=item.get_absolute_url(), type='auto')
