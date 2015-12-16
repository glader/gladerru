# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from random import choice
from hashlib import md5

from django.http import Http404, HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from django.core.mail import mail_admins

from .models import LandingPage, Stat


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        try:
            page = LandingPage.objects.get(slug=kwargs['slug'])
        except LandingPage.DoesNotExist:
            raise Http404

        template = get_template('lp/' + page.template)
        source = template.template.source

        params = {}
        for res in re.findall(r'variant_(\S+)\s?==\s?[\'\"]([^\'\"]+)[\'\"]', source, re.MULTILINE):
            params.setdefault(res[0], set()).add(res[1])

        current_params = [(k, choice(list(params[k]))) for k in sorted(params.keys())]
        hash = md5('&'.join('%s=%s' % param for param in current_params)).hexdigest()

        stat, _ = Stat.objects.get_or_create(
            page=page,
            hash=hash,
            defaults={'params': current_params}
        )

        stat.views += 1
        stat.save()

        context = {'variant_' + k: v for k, v in current_params}
        context['hash'] = hash

        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        try:
            page = LandingPage.objects.get(slug=kwargs['slug'])
        except LandingPage.DoesNotExist:
            raise Http404

        stat, _ = Stat.objects.get_or_create(page=page, hash=request.POST['hash'])
        stat.actions += 1
        stat.save()

        mail_admins(
            'glader.ru: заполнена форма',
            'Заполнена форма на странице http://glader.ru%s\n' % page.get_absolute_url() +
            '\n'.join('%s=%s' % (k, v) for k, v in request.POST.items())
        )

        return HttpResponse('Ваши данные сохранены. Спасибо за обращение', content_type='text/html; charset=utf-8')
