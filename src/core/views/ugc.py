# -*- coding: utf-8 -*-

from datetime import datetime
import re
import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from core.forms import PostForm, LoginForm, RegistrationForm
from core.models import Post, Photo, Tag, Keyword, NewsCategory
from core.utils.common import slug
from core.views.common import render_to_response
from core.decorators import time_slow, posts_feed


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
@posts_feed(template="category.html")
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

    return render_to_response(request, 'post.html', context)


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


def get_user(username):
    return get_object_or_404(User, username=username)


def get_section_objects(user, section):
    if section == 'posts':
        objects = Post.objects.filter(author=user).order_by('-date_created')

    elif section == 'draft':
        objects = Post.all.filter(author=user, status__in=('save', 'deferred')).order_by('-date_created')

    elif section == 'photos':
        objects = Photo.objects.filter(author=user).order_by('-date_created')

    else:
        raise Http404()

    return objects


@time_slow
def user_post(request, user, post_id):
    post = get_object_or_404(Post, pk=post_id, hidden=False)

    return HttpResponseRedirect(post.get_absolute_url())


def process_keywords(post):
    u"""Заменяет слова на ссылки по таблице Keywords"""
    words = list(Keyword.objects.all())
    words.sort(key=lambda word: len(word.keyword), reverse=True)
    for word in words:
        if word.keyword in post.content:
            content = re.sub(u'(<[^>]+)%s' % word.keyword, lambda res: res.group(1) + u'ЪЪЪЪЪ', post.content, re.I)
            content = re.sub(
                u'(?<!>)%s(?!<)' % word.keyword,
                u'<a href="%s" title="ЪЪЪЪЪ">%s</a>' % (word.url, word.keyword),
                content,
                1,
            )
            content = re.sub(
                u'(?<!>)%s(?!<)' % word.keyword,
                u'<span>%s</span>' % word.keyword,
                content,
            )
            post.content = re.sub(u'ЪЪЪЪЪ', word.keyword, content)


@login_required
def new_post(request):
    post = Post(title='', content='', comment_count=0,
                status='save', author=request.user, ip=request.META['REMOTE_ADDR'])
    post.save()
    return HttpResponseRedirect(reverse('edit_post', args=[post.id]))


@login_required
def edit_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if not post.can_edit(user):
        raise Http404

    if 'action' in request.POST:
        form = PostForm(request.POST, request.FILES, user=user, post=post)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.category = form.cleaned_data['category']
            post.geography = form.cleaned_data['geography']

            post.slug = slug(post.title)
            process_keywords(post)

            # Теги
            post.tags.clear()
            post.tags.add(*form.cleaned_data['tags'])

            video_tag = Tag.objects.get(name='video')
            if ('<youtube' in post.content or '<embed' in post.content) and \
                    video_tag not in form.cleaned_data['tags']:
                        post.tags.add(video_tag)

            # Статус
            status = {u'Удалить': 'del', u'Опубликовать': 'pub', u'В черновики': 'save'}.get(request.POST['action'])
            if status:
                post.status = status

            # Отложенная публикация
            if status == 'pub' and form.cleaned_data['deferred_datetime']:
                post.status = 'deferred'
                post.date_created = form.cleaned_data['deferred_datetime']

            # Картинка
            if 'picture' in form.cleaned_data and form.cleaned_data['picture']:
                image = Photo(title=form.cleaned_data['pic_title'], author=user, post=post)
                image.save()

                image.image.save('', form.cleaned_data['picture'])

                post.content += ' <glader pic="%s">' % image.id

            post.rebuild_tags()

            if request.POST['action'] == u'Просмотр':
                post.preview = True
            else:
                if request.POST['action'] == u'Опубликовать':
                    for p in Photo.objects.filter(post=post):
                        p.tags.clear()
                        p.tags.add(*form.cleaned_data['tags'])
                    return HttpResponseRedirect(post.get_absolute_url())

                elif request.POST['action'] == u'Удалить':
                    return HttpResponseRedirect(user.get_absolute_url())
                else:
                    return HttpResponseRedirect(reverse('edit_post', args=[post.id]))
        else:
            pass
    else:
        tags = post.tags.all().order_by('type', '-size')
        initial = {'post': post.id,
                   'title': post.title,
                   'content': post.content,
                   'tags': [t.title for t in tags],
                   }
        form = PostForm(user=user, initial=initial, post=post)

    pictures = Photo.objects.filter(post=post)

    return render_to_response(request,
                              'post_new.html',
                              {'post': post, 'form': form, 'pictures': pictures}
                              )


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
