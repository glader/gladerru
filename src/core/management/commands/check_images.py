# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag, Comment

from django.core.management.base import NoArgsCommand

from core.models import Post


def sanitizeHTML(value, mode='none'):
    """ Удаляет из value html-теги.
        Если mode==none - все теги
        Если mode==strict - все теги кроме разрешенных
    """
    if mode == 'strict':
        valid_tags = 'p i strong b u a h1 h2 h3 h4 pre br div span img blockquote glader cut object param embed'.split()
    else:
        valid_tags = []

    valid_attrs = 'href src pic user page class text title alt'.split()
    # параметры видеороликов
    valid_attrs += 'width height classid codebase id name value flashvars allowfullscreen allowscriptaccess quality src type bgcolor base seamlesstabbing swLiveConnect pluginspage data frameborder'.split()
    print "SANITIZE"
    print value

    soup = BeautifulSoup(value)
    # for comment in soup.findAll(
    #    text=lambda text: isinstance(text, HtmlComment)):
    #    comment.extract()

    for tag in soup.recursiveChildGenerator():
        if isinstance(tag, Tag) and tag.name in valid_tags:
            tag.attrs = [(attr, val) for attr, val in tag.attrs
                         if attr in valid_attrs]
        elif isinstance(tag, Comment):
            tag.extract()
        else:
            tag.hidden = True

    print soup
    result = soup.renderContents().decode('utf8')
    return result


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for post in Post.objects.all():
            try:
                tree = BeautifulSoup(post.content, "html5lib")

                for tag in tree.find_all('img'):
                    image = tag.get('src')
                    if 'thumb' not in image:
                        if not image.startswith('http') or 'glader.ru' in image:
                            print post.id, '\t', tag.get('src')
            except Exception, e:
                print e
