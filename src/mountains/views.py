# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView, DetailView

from .models import Mountain, Region


class MountainsView(TemplateView):
    template_name = 'mountains/mountains.html'

    def get_context_data(self, **kwargs):
        context = super(MountainsView, self).get_context_data(**kwargs)
        context.update(get_mountains())
        return context


class RegionView(DetailView):
    model = Region
    template_name = 'mountains/mountains.html'

    def get_context_data(self, **kwargs):
        context = super(RegionView, self).get_context_data(**kwargs)
        context.update(get_mountains(region=context['object']))
        return context


class MountainView(DetailView):
    model = Mountain
    template_name = 'mountains/mountain.html'

    def get_context_data(self, **kwargs):
        context = super(MountainView, self).get_context_data(**kwargs)
        context.update({
            'page_identifier': 'mountain_%s' % context['object'].id,
            'YAMAPS_API_KEY': settings.YAMAPS_API_KEY
        })
        return context


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

    return {'regions': regions, 'mountains': mountains, 'YAMAPS_API_KEY': settings.YAMAPS_API_KEY}
