# -*- coding: utf-8 -*-
from datetime import date, timedelta

from django.core.management.base import NoArgsCommand

from core.models import Profile, UserVisitStat


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        day = date.today() - timedelta(1)
        for p in Profile.objects.filter(last_visit__gt=day, last_visit__lt=day + timedelta(1)):
            UserVisitStat.objects.create(user=p.user, day=day)
