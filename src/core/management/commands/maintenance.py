# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.core.management.base import NoArgsCommand
from django.db import connection

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        cursor = connection.cursor()
        two_weeks = (datetime.now()-timedelta(14)).date().strftime("%Y-%m-%d")

        cursor.execute("DELETE FROM core_news WHERE date_created <='%s'" % two_weeks)
        cursor.execute("DELETE un FROM core_usernews un LEFT JOIN core_news n ON un.news_id=n.id WHERE n.id IS NULL")
        
        cursor.execute("DELETE FROM django_session WHERE expire_date <='%s'" % two_weeks)
        
        cursor.execute("SHOW TABLES")
        result = cursor.fetchall()
        for t in result:
            cursor.execute("OPTIMIZE TABLE %s" % t[0])
            
