# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext, loader
from django.http import HttpResponse


def render_to_response(request, template_name, context_dict=None, cookies=None):
    html = render_to_string(request, template_name, context_dict or {})
    response = HttpResponse(html)
    for k, v in (cookies or {}).items():
        response.set_cookie(k, v)
    return response


def render_to_string(request, template_name, context_dict=None):
    context = RequestContext(request, context_dict or {})
    t = loader.get_template(template_name)
    return t.render(context)
