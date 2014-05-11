# -*- coding: utf-8 -*-
from django.conf import settings


def core(request):
    context = {
        'STATIC_URL': settings.STATIC_URL,
    }

    if request.user.is_authenticated():
        context['profile'] = request.user.get_profile()

    return context
