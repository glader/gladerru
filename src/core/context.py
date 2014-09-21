# -*- coding: utf-8 -*-
from django.conf import settings


def profile(request):
    if request.user.is_authenticated():
        return {'profile': request.user.get_profile()}
    else:
        return {}


def domain(request):
    return {'DOMAIN': settings.DOMAIN}
