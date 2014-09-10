# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.conf import settings
from models import Post, Tag


class AllPosts(Feed):
    """ Свежие сообщения в блоге """
    title = u"Glader.ru: последние сообщения"
    link = "http://%s" % settings.DOMAIN
    description = "Свежие сообщения на сайте сноуборд-энциклопедии Glader.ru"
    title_template = 'feeds/all_title.html'
    description_template = 'feeds/all_description.html'

    def items(self):
        return Post.objects.filter(status='pub', type='post').order_by('-date_created')[:20]

    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""

    def item_link(self, item):
        return item.get_absolute_url()
