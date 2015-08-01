# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from .models import Discount


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        exclude = ('user', 'date_created')

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        for f in self.base_fields.values():
            f.error_messages['required'] = 'Это поле обязательно для заполнения'
