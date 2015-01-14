# -*- coding: utf-8 -*-

from datetime import datetime
import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView
from django.core.mail import mail_admins

from core.forms import PostForm, LoginForm, RegistrationForm
from core.models import Post, NewsCategory
from core.views.common import render_to_response
from core.decorators import class_view_decorator


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


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categories'] = list(NewsCategory.objects.all().order_by('order'))
        fresh = {
            'title': u'Свежее',
            'posts': list(Post.objects.filter(status='pub', type='post').order_by('-date_created')[:4])
        }
        fresh['posts'].sort(key=lambda post: (post.is_sticky and 2 or 1, post.date_created), reverse=True)
        fresh_posts = [post.id for post in fresh['posts']]
        for category in context['categories']:
            category.posts = list(
                Post.objects.filter(status='pub', type='post', category=category)
                .exclude(id__in=fresh_posts).order_by('-date_created')[:4]
            )
            category.posts.sort(key=lambda post: (post.is_sticky and 2 or 1, post.date_created), reverse=True)
            category.start = timestamp(category.posts[-1].date_created)
        context['categories'].insert(0, fresh)
        return context


class CategoryView(TemplateView):
    template_name = "core/category.html"
    POSTS_PER_CATEGORY = 20

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(NewsCategory, slug=kwargs['slug'])

        start = parse_timestamp(self.request.GET.get('start'))
        context['posts'] = Post.objects\
            .filter(hidden=False, category=context['category'], type='post') \
            .exclude(icon='').order_by('-date_created')
        if start:
            context['posts'] = context['posts'].filter(date_created__lt=start)

        context['posts'] = context['posts'][:self.POSTS_PER_CATEGORY + 1]
        if len(context['posts']) == self.POSTS_PER_CATEGORY + 1:
            context['start'] = timestamp(context['posts'][self.POSTS_PER_CATEGORY].date_created)
            context['posts'] = context['posts'][:self.POSTS_PER_CATEGORY]
        return context


def post_view(request, slug, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not (post.status == 'pub' or (request.user.is_authenticated() and post.can_edit(request.user))):
        raise Http404

    context = {'post': post,
               'can_edit': post.can_edit(request.user),
               'page_identifier': 'post_%s' % post.id,
               }

    return render_to_response(request, 'core/post.html', context)


def post_htm_view(request, category_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return post_view(request, category_slug, post.id)


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
    queryset = Post.all.all()
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update posts """
        obj = self.get_object()
        if obj.author == self.request.user or self.request.user.is_superuser:
            return super(EditPostView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            if request.POST.get('action') == u'Опубликовать':
                post = self.get_object()
                post.status = 'pub'
                post.save()
                return HttpResponseRedirect(post.get_absolute_url())

            if request.POST.get('action') == u'Забанить':
                post = self.get_object()
                post.status = 'ban'
                post.save()
                return HttpResponseRedirect(post.get_absolute_url())

        return super(EditPostView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        obj = self.get_object()
        return reverse('post', args=[obj.category.slug, obj.id])


class TempPostView(EditPostView):
    def get_object(self, **kwargs):
        posts = Post.objects.filter(status='pub', type='post', icon='').order_by('-date_created')
        if self.request.GET.get('category'):
            posts = posts.filter(category__slug=self.request.GET.get('category'))
        return posts[0]

    def get_success_url(self):
        return reverse('temp_post') + '?category=' + self.request.GET.get('category', '')


###############################################################################
# Авторизация

def registration(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            auth.login(request, form.user)
            next = request.POST.get('next') or form.user.get_absolute_url()
            if 'referer' in request.session:
                profile = form.user.get_profile()
                profile.referer = request.session['referer']
                profile.save()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps({'success': True, 'next': next}))
            else:
                return HttpResponseRedirect(next)

        elif request.is_ajax():
            return JsonErrorResponse(form.str_errors())

    else:
        form = RegistrationForm(initial={'next': request.GET.get('next')})

    return render_to_response(request, 'registration/login.html', {'registration_form': form,
                                                                   'login_form': LoginForm()})


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            auth.login(request, user)
            next = request.POST.get('next') or form.user.get_absolute_url()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps({'success': True, 'next': next}))
            else:
                return HttpResponseRedirect(next)

        elif request.is_ajax():
            return JsonErrorResponse(form.str_errors())

    else:
        login_form = LoginForm(initial={'next': request.GET.get('next')})

    registration_form = RegistrationForm(initial=request.GET)
    return render_to_response(request, 'registration/login.html', locals())
