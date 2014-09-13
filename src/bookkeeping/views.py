# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.http import Http404

from .models import Record


class Overview(CreateView):
    model = Record
    template_name = 'bookkeeping/index.html'
    success_url = '/bookkeeping/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super(Overview, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Overview, self).get_context_data(**kwargs)
        records = list(Record.objects.all())
        total = {'glader': 0, 'skyslayer': 0}
        for record in records:
            total[record.account] += record.amount

        context['records'] = records[:20]
        context['total'] = total
        context['difference'] = abs((total['glader'] - total['skyslayer']) / 2)
        return context
