# encoding: utf-8
from django import template

register = template.Library()


@register.filter
def good_or_bad(rating):
    if rating > 0:
        return "good"
    elif rating < 0:
        return "bad"
    else:
        return "zero"


@register.filter
def signed_number(number):
    if number > 0:
        return "+%d" % number
    else:
        return "%d" % number


@register.filter
def decimal_cut(value, numbers=1):
    format = "%%0.%df" % numbers
    return format % value
