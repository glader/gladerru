# coding: utf-8
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        two_weeks = (datetime.now() - timedelta(14)).date().strftime("%Y-%m-%d")

        cursor.execute("DELETE FROM django_session WHERE expire_date <='%s'" % two_weeks)

        cursor.execute("SHOW TABLES")
        result = cursor.fetchall()
        for t in result:
            cursor.execute("OPTIMIZE TABLE %s" % t[0])
