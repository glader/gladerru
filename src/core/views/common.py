# -*- coding: utf-8 -*-

from django.template import RequestContext, loader
from django.http import HttpResponse

def render_to_response(request, template_name, context_dict={}, cookies={}):
    html = render_to_string(request, template_name, context_dict)
    response = HttpResponse(html)
    for k, v in cookies.items():
        response.set_cookie(k, v)
    return response


def render_to_string(request, template_name, context_dict={}):
    context = RequestContext(request, context_dict)
    t = loader.get_template(template_name)
    return t.render(context)