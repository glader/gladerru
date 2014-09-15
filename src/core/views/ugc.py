# -*- coding: utf-8 -*-

from datetime import datetime
import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.core.mail import mail_admins

from core.forms import PostForm, LoginForm, RegistrationForm
from core.models import Post, NewsCategory
from core.utils.common import slug
from core.views.common import render_to_response
from core.decorators import time_slow, posts_feed, class_view_decorator


class JsonResponse(HttpResponse):
    """ HttpResponse descendant, which return response with ``application/json`` mimetype. """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


class JsonErrorResponse(JsonResponse):
    """ Error message """
    def __init__(self, data):
        super(JsonErrorResponse, self).__init__({'error': data})


###############################################################################

def parse_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts))
    except Exception:
        return None


def timestamp(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds())


@time_slow
@posts_feed(template="index.html")
def index(request):
    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(status='pub', type='post').order_by('-date_created')
    if start:
        posts = posts.filter(date_created__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
    }
    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].date_created)
        context['posts'] = context['posts'][:10]
    return context


@time_slow
@posts_feed(template="core/category.html")
def category_view(request, slug):
    category = get_object_or_404(NewsCategory, slug=slug)

    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(hidden=False, category=category, type='post').order_by('-date_created')
    if start:
        posts = posts.filter(date_created__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
        'category': category,
    }
    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].date_created)
        context['posts'] = context['posts'][:10]
    return context


@time_slow
def post_view(request, slug, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not (post.status == 'pub' or (request.user.is_authenticated() and post.can_edit(request.user))):
        raise Http404

    context = {'post': post,
               'can_edit': post.can_edit(request.user),
               'page_identifier': 'post_%s' % post.id,
               }

    return render_to_response(request, 'core/post.html', context)


###############################################################################
# UGC
###############################################################################


@time_slow
@posts_feed()
def all(request):
    """ Свежие записи во всех блогах """
    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(status='pub', type='post').order_by('-date_created')
    if start:
        posts = posts.filter(date_created__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
        'title': u'Все сообщения',
        'menu_item': 'all_posts',
    }

    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].date_created)
        context['posts'] = context['posts'][:10]
    return context


@time_slow
def user_post(request, user, post_id):
    post = get_object_or_404(Post, pk=post_id, hidden=False)
    return HttpResponseRedirect(post.get_absolute_url())


@class_view_decorator(login_required)
class AddPostView(CreateView):
    template_name = 'core/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.slug = slug(post.title)
        if self.request.user.is_superuser:
            post.status = 'pub'
            post.save()
            self.success_url = reverse('post', args=[post.category.slug, post.id])
        else:
            post.status = 'save'
            post.save()
            self.success_url = reverse('edit_post', args=[post.id])

        mail_admins('New post', self.success_url)

        return super(AddPostView, self).form_valid(form)


class EditPostView(UpdateView):
    template_name = 'core/post_edit.html'
    queryset = Post.objects.all()
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update posts """
        obj = self.get_object()
        if (obj.author == self.request.user and obj.status == 'save') or self.request.user.is_superuser:
            return super(EditPostView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_success_url(self):
        obj = self.get_object()
        return reverse('post', args=[obj.category.slug, obj.id])


class TempPostView(EditPostView):
    def get_object(self):
        return Post.objects.filter(status='pub', type='post', icon='').order_by('-date_created')[0]

    def get_success_url(self):
        return reverse('temp_post')


###############################################################################
# Авторизация

def registration(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            auth.login(request, form.user)
            retpath = request.POST.get('retpath') or form.user.get_absolute_url()
            if 'referer' in request.session:
                profile = form.user.get_profile()
                profile.referer = request.session['referer']
                profile.save()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps({'success': True, 'retpath': retpath}))
            else:
                return HttpResponseRedirect(retpath)

        elif request.is_ajax():
            return JsonErrorResponse(form.str_errors())

    else:
        form = RegistrationForm(initial={'retpath': request.GET.get('next')})

    return render_to_response(request, 'registration/login.html', {'registration_form': form,
                                                                   'login_form': LoginForm()})


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            auth.login(request, user)
            retpath = request.POST.get('retpath') or form.user.get_absolute_url()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps({'success': True, 'retpath': retpath}))
            else:
                return HttpResponseRedirect(retpath)

        elif request.is_ajax():
            return JsonErrorResponse(form.str_errors())

    else:
        login_form = LoginForm(initial={'retpath': request.GET.get('next')})

    registration_form = RegistrationForm(initial=request.GET)
    return render_to_response(request, 'registration/login.html', locals())
