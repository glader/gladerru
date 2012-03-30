# -*- coding: utf-8 -*-

import re
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from core.models import Post, Photo, Tag

###############################################################################
# Редиректы для старых урлов


def get_username(request):
        if not 'HTTP_HOST' in request.META:
                return
        result = re.match('([\w\d_-]+)\.%s' % settings.DOMAIN, request.META['HTTP_HOST'])
        if result and result.group(1) != 'www':
            return result.group(1)

        return


def add_domain(url):
    return "http://%s%s" % (settings.DOMAIN, url)


def old_my(request):
    return HttpResponsePermanentRedirect(add_domain(reverse('user_staff', args=[get_username(request), 'posts'])))


def old_my_posts(request):
    return HttpResponsePermanentRedirect(add_domain(reverse('user_staff', args=[get_username(request), 'posts'])))


def old_user_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponsePermanentRedirect(post.get_absolute_url())


def old_pic(request, id):
    pic = get_object_or_404(Photo.objects.filter(pk=id))
    return HttpResponsePermanentRedirect(pic.get_absolute_url())


def old_post_category(request, category_name):
    tag = get_object_or_404(Tag, name=category_name)
    return HttpResponsePermanentRedirect(tag.get_absolute_url())


def old_blog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponsePermanentRedirect(post.get_absolute_url())


def old_forum_profile(request):
    user = get_object_or_404(User, pk=request.GET.get('u'))
    return HttpResponsePermanentRedirect(user.get_absolute_url())


def old_best(request):
    return HttpResponsePermanentRedirect("/" + (request.META['QUERY_STRING'] and "?%s" % request.META['QUERY_STRING'] or ""))
