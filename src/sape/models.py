# -*- coding: utf-8 -*-
from django.db import models


class Link(models.Model):
    link_id = models.CharField(verbose_name=u'ID', max_length=50, unique=True)
    status = models.CharField(verbose_name=u'Статус', max_length=50)
    txt = models.CharField(verbose_name=u'Текст', max_length=255)
    url = models.CharField(verbose_name=u'Ссылка', max_length=255)
    page = models.CharField(verbose_name=u'Урл страницы', max_length=255, db_index=True)

    def __unicode__(self):
        html = self.txt.replace('#a#', '<a href="%s" target="_blank">' % self.url).replace('#/a#', '</a>')
        return html

    class Meta:
        verbose_name = u"Ссылка"
        verbose_name_plural = u"Ссылки"
