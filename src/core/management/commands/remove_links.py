# coding: utf-8
from bs4 import BeautifulSoup, element

from django.core.management.base import NoArgsCommand

from core.models import Post


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for post in Post.objects.all():
            if '/people/' not in post.content:
                continue

            # print post.content.encode('utf8')[:600]

            soup = BeautifulSoup(post.content.encode('utf8'), from_encoding='utf8')
            for tag in soup.find_all('a'):
                if '/people/' in tag.attrs.get('href', ''):
                    tag.replace_with(tag.text)

            for tag in soup.recursiveChildGenerator():
                if isinstance(tag, element.Tag) and tag.name in ('html', 'head', 'body'):
                    tag.hidden = True

            content = soup.encode_contents(indent_level=2).decode('utf8')\
                .replace('<html><body>', '').replace('</body></html>', '')
            # print content.encode('utf8')[:600]

            if content != post.content:
                post.content = content
                post.save()
                print "http://glader.ru" + post.get_absolute_url()
