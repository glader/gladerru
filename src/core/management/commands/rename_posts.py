# coding: utf-8

from django.db import connection
from django.core.management.base import BaseCommand

from core.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute(
            'SELECT DISTINCT p1.slug FROM core_post p1 JOIN core_post p2 ON p1.id < p2.id AND p1.slug=p2.slug'
        )

        for row in cursor.fetchall():
            posts = Post.objects.filter(slug=row[0]).order_by('id')
            for n, post in enumerate(posts[1:], start=2):
                post.title += ' %s' % n
                post.slug += '-%s' % n
                post.save()
