# -*- coding: utf-8 -*-
import re
import os
from datetime import datetime
from django.conf import settings
from django.utils.html import strip_spaces_between_tags as short
import logging
from time import time


class UserReferer:
    def process_request(self, request):
        if request.META.get('HTTP_REFERER') and not request.user.is_authenticated() and not 'referer' in request.session:
            request.session['referer'] = request.META['HTTP_REFERER']


class LastLogin:
    def process_request(self, request):
        if request.user.is_authenticated():
            user = request.user.get_profile()
            user.last_visit = datetime.now()
            user.save()


class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if not settings.DEBUG and 'text/html' in response['Content-Type']:
            response.content = short(response.content)
        return response
