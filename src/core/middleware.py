from __future__ import unicode_literals
from django.http import HttpResponsePermanentRedirect

from core.models import Redirect


class UserReferer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('HTTP_REFERER') and not request.user.is_authenticated \
                and 'referer' not in request.session:
            request.session['referer'] = request.META['HTTP_REFERER']

        response = self.get_response(request)

        return response


class Redirection:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            destination = Redirect.find(request.META['PATH_INFO'])
            if destination:
                return HttpResponsePermanentRedirect(destination)

        return response