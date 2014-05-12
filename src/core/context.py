# -*- coding: utf-8 -*-


def profile(request):
    if request.user.is_authenticated():
        return {'profile': request.user.get_profile()}
    else:
        return {}
