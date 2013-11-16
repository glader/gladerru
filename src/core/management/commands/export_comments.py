# -*- coding: utf-8 -*-
from itertools import groupby
from django.core.management.base import NoArgsCommand

from core.models import Comment

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:dsq="http://www.disqus.com/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:wp="http://wordpress.org/export/1.0/"
>
  <channel>"""

        comments = Comment.all.all()

        for comment in comments:
            item = comment.item
            if not item: continue
            if not comment.content or len(comment.content) < 5: continue

            print "<item><title><![CDATA[%s]]></title>" % item.title.encode('utf8')
            print "<link>http://glader.ru%s</link>" % item.get_absolute_url()
            print "<content:encoded></content:encoded>"
            print "<dsq:thread_identifier>%s_%s</dsq:thread_identifier>" % (item.__class__.__name__.lower(), item.id)
            print "<wp:post_date_gmt></wp:post_date_gmt>"
            print "<wp:comment_status>open</wp:comment_status>"
            print "<wp:comment>"
            print "<wp:comment_id>%s</wp:comment_id>" % comment.id
            print "<wp:comment_author>%s</wp:comment_author>" % comment.author.username.encode('utf8')
            print "<wp:comment_author_email>%s</wp:comment_author_email>" % comment.author.email
            print "<wp:comment_author_url></wp:comment_author_url>"
            print "<wp:comment_author_IP></wp:comment_author_IP>"
            print "<wp:comment_date_gmt>%s</wp:comment_date_gmt>" % comment.date_created.strftime("%Y-%m-%d %H:%M:%S")
            print "<wp:comment_content><![CDATA[%s]]></wp:comment_content>" % comment.content.encode('utf8')
            print "<wp:comment_approved>1</wp:comment_approved>"
            print "<wp:comment_parent>0</wp:comment_parent></wp:comment></item>"

        print "</channel></rss>"
