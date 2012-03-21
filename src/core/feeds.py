# -*- coding:utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from models import Post, Comment, Tag

class BestPosts(Feed):
    """ Лучшие сообщения в блоге """
    title = u"Glader.ru: лучшие сообщения"
    link = "http://%s" % settings.DOMAIN
    description = "Лучшие сообщения на сайте сноуборд-энциклопедии Glader.ru"
    
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


class NewComments(Feed):
    """ Свежие комментарии в блоге """
    title = u"Glader.ru: последние комментарии"
    link = "http://%s" % settings.DOMAIN
    description = "Свежие комментарии на сайте сноуборд-энциклопедии Glader.ru"

    def items(self):
        return Comment.objects.all().order_by('-date_created')[:50]
    
    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""

from core.views.ugc import get_section_objects
class Users(Feed):
    def link(self):
        return "%s/%s" % (self.user.get_absolute_url(), self.section) 
    
    def get_object(self, bits):
        # In case of "/feeds/users/glader/posts", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 2:
            raise ObjectDoesNotExist
        self.section = bits[1]
        self.user = User.objects.get(username=bits[0]) 
        return self.user
    
    def items(self, obj):
        if self.section not in ('posts', 'photos'):
            raise ObjectDoesNotExist
        return get_section_objects(obj, self.section).order_by('-date_created')[:20]

    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""


class Tags(Feed):
    def link(self):
        return self.tag.get_absolute_url() 
    
    def get_object(self, bits):
        # In case of "/feeds/tag/otchet", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        self.tag = get_object_or_404(Tag, name=bits[0])
        return self.tag
    
    def items(self, obj):
        from core.templatetags.content import make_tag_pages
        context = make_tag_pages(obj)
        return context['items'][:20]

    def item_pubdate(self, item):
        return item.date_created

    def item_author_name(self, item):
        author = item.author
        return author and author.first_name or ""
