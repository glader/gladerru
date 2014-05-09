# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.conf import settings
from models import Post, Tag


class BestPosts(Feed):
    """ Лучшие сообщения в блоге """
    title = u"Glader.ru: лучшие сообщения"
    link = "http://%s" % settings.DOMAIN
    description = "Лучшие сообщения на сайте сноуборд-энциклопедии Glader.ru"
    title_template = 'feeds/best_title.html'
    description_template = 'feeds/best_description.html'

    def items(self, obj):
        return Post.objects.filter(best__isnull=False, status='pub').order_by('-best')[:20]

    def item_pubdate(self, item):
        return item.best

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""

    def item_link(self, item):
        if item.type == 'post':
            return item.get_absolute_url()
        else:
            return item.item.get_absolute_url()


class AllPosts(Feed):
    """ Свежие сообщения в блоге """
    title = u"Glader.ru: последние сообщения"
    link = "http://%s/all" % settings.DOMAIN
    description = "Свежие сообщения на сайте сноуборд-энциклопедии Glader.ru"
    title_template = 'feeds/all_title.html'
    description_template = 'feeds/all_description.html'

    def items(self):
        return Post.objects.filter(status='pub').order_by('-date_created')[:20]

    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""

    def item_link(self, item):
        if item.type == 'post':
            return item.get_absolute_url()
        else:
            return item.item.get_absolute_url()


class Tags(Feed):
    title_template = 'feeds/tags_title.html'
    description_template = 'feeds/tags_description.html'

    def get_object(self, request, tag_name):
        return get_object_or_404(Tag, name=tag_name)

    def items(self, obj):
        from core.templatetags.content import make_tag_pages
        context = make_tag_pages(obj)
        return context['items'][:20]

    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""

    def link(self, obj):
        return obj.get_absolute_url()
