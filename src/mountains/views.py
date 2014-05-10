# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Mountain, Region
from core.views.common import render_to_response


def get_mountains(region=None):
    if region:
        regions = [region]
        mountains = Mountain.objects.filter(region=region)
    else:
        regions = Region.objects.all()
        mountains = Mountain.objects.all()

    regions_dict = dict((r.id, r) for r in regions)
    for m in mountains:
        if not hasattr(regions_dict[m.region_id], 'mountains'):
            regions_dict[m.region_id].mountains = []
        regions_dict[m.region_id].mountains.append(m)

    return {'regions': regions, 'mountains': mountains}


def mountains(request):
    context = get_mountains()
    context['YAMAPS_API_KEY'] = settings.YAMAPS_API_KEY
    return render_to_response(request, 'mountains.html', context)


def mountain(request, name):
    mountain = get_object_or_404(Mountain, name=name)
    return render_to_response(request, 'mountain.html', {'mountain': mountain, 'page_identifier': 'mountain_%s' % mountain.id})


def region(request, region_id):
    region = get_object_or_404(Region, pk=region_id)
    return render_to_response(request, 'mountains.html', get_mountains(region))
