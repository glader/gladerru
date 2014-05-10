# -*- coding: utf-8 -*-
from itertools import groupby

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from .forms import DiscountForm
from .models import Discount


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


def discounts(request):
    discounts = [(k, list(v)) for k, v in groupby(Discount.objects.all().order_by('city', 'card', 'discount'), lambda d: d.city)]
    return render_to_response(request, 'discounts.html', {'discounts': discounts})


def discount_new(request):
    if not request.user.is_authenticated():
        raise Http404

    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.user = request.user
            discount.save()
            return HttpResponseRedirect(reverse('discounts'))
    else:
        form = DiscountForm()

    return render_to_response(request, 'discount_form.html', {'form': form})


def discount_edit(request, discount_id):
    if not request.user.is_authenticated():
        raise Http404

    discount = get_object_or_404(Discount, pk=discount_id)
    if not (request.user == discount.user or request.user.get_profile().is_moderator):
        raise Http404

    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('discounts'))
    else:
        form = DiscountForm(instance=discount)

    return render_to_response(request, 'discount_form.html', {'form': form})


def discount_delete(request, discount_id):
    if not request.user.is_authenticated():
        raise Http404

    discount = get_object_or_404(Discount, pk=discount_id)
    if not (request.user == discount.user or request.user.get_profile().is_moderator):
        raise Http404

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        discount.delete()
        return HttpResponseRedirect(reverse('discounts'))

    return render_to_response(request, 'discount_delete.html', {'discount': discount})
