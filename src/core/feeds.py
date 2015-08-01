# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.conf import settings
from models import Post


class AllPosts(Feed):
    """ Свежие сообщения в блоге """
    title = 'Glader.ru: последние сообщения'
    link = 'http://%s' % settings.DOMAIN
    description = 'Свежие сообщения на сайте сноуборд-энциклопедии Glader.ru'
    title_template = 'feeds/all_title.html'
    description_template = 'feeds/all_description.html'

    def items(self):
        return Post.objects.filter(status='pub', type='post').order_by('-date_created')[:20]

    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ''

    def item_link(self, item):
        return item.get_absolute_url()
