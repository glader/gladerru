from __future__ import unicode_literals
from django.http import HttpResponsePermanentRedirect

from core.models import Redirect


class UserReferer:
    def process_request(self, request):
        if request.META.get('HTTP_REFERER') and not request.user.is_authenticated() \
                and 'referer' not in request.session:
            request.session['referer'] = request.META['HTTP_REFERER']


class Redirection:
    def process_response(self, request, response):
        if response.status_code == 404:
            destination = Redirect.find(request.META['PATH_INFO'])
            if destination:
                return HttpResponsePermanentRedirect(destination)

        return response
