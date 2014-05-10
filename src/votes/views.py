# -*- coding: utf-8 -*-

from datetime import datetime
import simplejson

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import PostVoteForm
from .models import ItemVote
from .templatetags.content import good_or_bad, signed_number


class JsonResponse(HttpResponse):
    """ HttpResponse descendant, which return response with ``application/json`` mimetype. """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


class JsonErrorResponse(JsonResponse):
    """ Error message """
    def __init__(self, data):
        super(JsonErrorResponse, self).__init__({'error': data})


@login_required
def add_post_vote(request):
    user = request.user
    form = PostVoteForm(request.GET, user=user)
    if form.is_valid():
        post = form.cleaned_data['post']
        add_vote(post, user, request.META['REMOTE_ADDR'])
        result = {
            'success': True,
            'vote_class': 'rating_' + good_or_bad(post.rating),
            'rating': str(signed_number(post.rating))
        }

    else:
        if 'retpath' in request.GET:
            return HttpResponseRedirect(request.GET['retpath'])
        else:
            return JsonErrorResponse(form.str_errors())

    if 'retpath' in request.GET:
        return HttpResponseRedirect(request.GET['retpath'])
    else:
        return HttpResponse(simplejson.dumps(result))


def add_vote(post, user, ip):
    vote = ItemVote(item=post, user=user, vote=1, ip=ip)
    vote.save()

    if post.rating:
        post.rating += 1
    else:
        post.rating = 1

    if hasattr(post, 'best') and not post.best and post.rating >= settings.MAIN_PAGE_LEVEL:
        post.best = datetime.now()

    post.save()
