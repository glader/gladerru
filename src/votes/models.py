# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ItemVote(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь')
    vote = models.IntegerField(verbose_name='Оценка')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    ip = models.CharField(verbose_name='IP', null=True, blank=True, max_length=30)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey()

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class VoteMixin(object):
    pk = None
    author = None

    def get_vote(self, user):
        """ Возвращает оценку, выставленную элементу юзером. None, если не голосовал """
        # FIXME: добавить votes = generic.GenericRelation(ItemVote)
        if user and user.is_authenticated():
            votes = ItemVote.objects.filter(content_type__pk=26, object_id=self.pk, user=user)
            if votes:
                return reduce(lambda x, y: x + y, [v.vote for v in votes])
        return None

    def can_vote(self, user):
        if not user:
            return False
        if not user.is_authenticated():
            return False
        if user.get_profile().is_moderator:
            return True
        if hasattr(self, 'author') and self.author == user:
            return False
        return self.get_vote(user) is None
