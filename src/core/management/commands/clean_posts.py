# coding: utf-8
import bs4
import re

from django.core.management.base import BaseCommand

from core.models import Post


def drop_empty_tag(tag):
    empty = True
    for child in tag.contents:
        if isinstance(child, bs4.element.NavigableString):
            if len(str(child).strip()) > 0:
                empty = False
                break
        else:
            empty = False
            break

    if empty:
        try:
            tag.extract()
        except Exception:
            tag.hidden = True


class Command(BaseCommand):
    def handle(self, *args, **options):
        for post in Post.objects.all():
            if not post.content:
                continue

            print(post.id)
            tree = bs4.BeautifulSoup(post.content.encode('utf8'), from_encoding='utf8')

            for tag in tree.find_all('br'):
                tag.extract()

            for tag in tree.find_all('strong'):
                drop_empty_tag(tag)

            for tag in tree.find_all('a'):
                drop_empty_tag(tag)

            for tag in tree.find_all('p'):
                drop_empty_tag(tag)

            html = tree.renderContents(prettyPrint=True, indentLevel=2)
            post.content = html
            post.save()

            post = Post.objects.get(pk=post.pk)
            post.content = re.sub('</?(html|body)>', '', post.content, re.U)
            post.save()
