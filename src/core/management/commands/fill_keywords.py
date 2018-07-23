# coding: utf-8
from itertools import chain

from django.core.management.base import BaseCommand

from core.models import Movie, Man, Studio, Word, Mountain, Keyword


class Command(BaseCommand):
    def handle(self, *args, **options):
        Keyword.objects.filter(type='auto').delete()

        for item in chain(Movie.objects.all(), Man.objects.all(), Studio.objects.all(),
                          Word.objects.all(), Mountain.objects.all()):
            Keyword.objects.create(keyword=item.title, url=item.get_absolute_url(), type='auto')
