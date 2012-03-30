# -*- coding: utf-8 -*-
from django.conf import settings
from core.forms import LoginForm, RegistrationForm


def default(request):
    context = {'user': None,
               'request': request,
               'debug': settings.DEBUG,
               'DOMAIN': settings.DOMAIN,
               'is_devel': settings.IS_DEVEL,
               }
    if request.user.is_authenticated():
        context['user'] = request.user
        context['profile'] = request.user.get_profile()

    return context
