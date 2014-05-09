# -*- coding: utf-8 -*-
from django.conf import settings


def default(request):
    context = {
        'user': None,
        'request': request,
        'debug': settings.DEBUG,
        'is_devel': settings.IS_DEVEL,
    }

    if request.user.is_authenticated():
        context['user'] = request.user
        context['profile'] = request.user.get_profile()

    return context
