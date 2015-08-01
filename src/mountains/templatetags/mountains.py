# encoding: utf-8
from __future__ import unicode_literals
from django import template

from ..views import get_mountains

register = template.Library()


@register.inclusion_tag('block_items_ul_list.html')
def mountains_list(region):
    return {'items': get_mountains(region)['mountains'][:20]}
