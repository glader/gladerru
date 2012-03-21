# -*- coding: utf-8 -*-
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django_glader_queue.models import Queue

from core.utils.common import process_template
from core.views.ugc import get_user_news

class Command(NoArgsCommand):
    def make_news_email(self, user, news):
        subject, content = process_template('email/news.html', {
                                            'user': user,
                                            'news': news
                                        })
        Queue.add_task('email', {'email': user.email,
                                 'subject': subject,
                                 'content': content})

    def handle_noargs(self, **options):
        week_ago = date.today() - timedelta(7)

        for user in User.objects.filter(email__isnull=False).exclude(email=''):
            profile = user.get_profile()
            if not profile.send_news:
                continue

            news = get_user_news(user)
            news = [day for day in news if day['date'] >= week_ago]
            if news:
                self.make_news_email(user, news)
                profile = user.get_profile()
                profile.unread_news_count = 0
                profile.save()

