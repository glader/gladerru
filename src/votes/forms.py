# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.db import models


class PostVoteForm(forms.Form):
    """ Голосование за пост """
    post = forms.CharField(label='Сообщение', error_messages={'required': 'Отсутствует код поста'})
    klass = forms.CharField(label='Тип элемента', error_messages={'required': 'Отсутствует тип элемента'})
    vote = forms.IntegerField(label='Оценка', error_messages={'required': 'Отсутствует оценка поста'})

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostVoteForm, self).__init__(*args, **kwargs)

    def clean_vote(self):
        vote = self.cleaned_data['vote']
        if not (self.user.get_profile().is_moderator or (vote == 1)):
            raise forms.ValidationError('Неправильная оценка')

        return vote

    def clean(self):
        all_models = models.get_models()
        current_model = None
        for model in all_models:
            if model._meta.model_name == self.cleaned_data['klass']:
                current_model = model
                break

        if not current_model:
            raise forms.ValidationError('Голосование за неизвестный тип контента')

        try:
            item = current_model.objects.get(pk=self.cleaned_data['post'])
        except current_model.DoesNotExist:
            raise forms.ValidationError('Голосование за неизвестный пост')

        if not item.can_vote(self.user):
            raise forms.ValidationError('Вы не можете голосовать за этот пост')

        self.cleaned_data['post'] = item
        return self.cleaned_data

    def errors_list(self):
        return [unicode(message) for k, l in self.errors.items() for message in l]

    def str_errors(self, divider='. '):
        return divider.join(self.errors_list())
