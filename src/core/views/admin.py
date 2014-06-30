# -*- coding: utf-8 -*-
from simplejson import dumps

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.models import Image


def moderator_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.get_profile().is_moderator:
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper


@csrf_exempt
@require_POST
def upload_photos(request):
    images = []
    for f in request.FILES.getlist("file"):
        obj = Image.objects.create(upload=f)
        images.append({"filelink": obj.upload.src()})
    return HttpResponse(dumps(images[0]), mimetype="application/json")
