# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
import calendar
import re
from xml.etree import ElementTree as ET
import simplejson

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from core.forms import PostForm, LoginForm, RegistrationForm, ProfileForm, PictureForm, \
    PhotoForm, sanitizeHTML
from core.models import Post, Photo, Comment, Tag, Keyword, TagsCloud
from core.templatetags.content import make_pages
from core.utils.common import process_template, slug
from core.views.common import render_to_response
from core.decorators import time_slow, auth_only, posts_feed
from core.utils.thumbnails import get_thumbnail_url, make_thumbnail
from core.tasks import new_post_announces, check_celery


class JsonResponse(HttpResponse):
    """ HttpResponse descendant, which return response with ``application/json`` mimetype. """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


class JsonErrorResponse(JsonResponse):
    """ Error message """
    def __init__(self, data):
        super(JsonErrorResponse, self).__init__({'error': data})


def best_posts(page=None):
    context = {'page': page,
               }
    context.update(make_pages(Post.objects.filter(status='pub').order_by('-best'),
                              10,
                              context.get('page')
                              ))
    return context


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
    if request.GET.get('celery'):
        check_celery.delay(request.GET.get('celery'))

    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(status='pub').order_by('-best')
    if start:
        posts = posts.filter(best__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
    }
    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].best)
        context['posts'] = context['posts'][:10]
    return context


@time_slow
@posts_feed(template="tag.html")
def tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    if tag.primary_synonim:
        return HttpResponsePermanentRedirect(tag.primary_synonim.get_absolute_url())

    item_ids = [int(id) for id in tag.posts.split(',')] if tag.posts else []
    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(hidden=False, id__in=item_ids).order_by('-date_created')
    if start:
        posts = posts.filter(best__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
        'tag': tag,
    }
    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].date_created)
        context['posts'] = context['posts'][:10]
    return context


def tags(request):
    tags = Tag.objects.filter(size__gt=1, type__gt=10).order_by('title')
    tags_cloud = TagsCloud(tags)
    tags_cloud.set_rel_sizes(12, 30)
    return render_to_response(request, 'tags_all.html', {'tags': tags})

###############################################################################
# UGC
###############################################################################


@time_slow
@posts_feed()
def all(request):
    """ Свежие записи во всех блогах """
    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(status='pub').order_by('-date_created')
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


@auth_only
@posts_feed()
def hidden(request):
    """ Вообще все посты, для модераторов """
    if not request.user.is_superuser:
        raise Http404

    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.all().order_by('-date_created')
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
@posts_feed()
def top_rating(request):
    u""" Лучшие за месяц """
    items = Post.objects \
                .filter(date_created__gte=date.today() - timedelta(days=30)) \
                .order_by('-rating')[:10]
    return {'posts': items, 'title': u'Лучшие за месяц', 'menu_item': 'rating'}


@time_slow
@posts_feed()
def top_discussed(request):
    u""" Самые обсуждаемые за месяц """
    items = Post.objects \
                .filter(date_created__gte=date.today() - timedelta(days=30), comment_count__gt=0) \
                .order_by('-comment_count')[:10]
    return {'posts': items, 'title': u'Самые обсуждаемые за месяц', 'menu_item': 'discussed'}


@posts_feed(template="faq.html")
def faq(request):
    u""" Посты с пометкой 'Вопрос' """
    start = parse_timestamp(request.GET.get('start'))
    posts = Post.objects.filter(tags__name='question').order_by('-date_created')
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


def schedule(request, year=None, month=None):
    u"""Календарь событий"""
    months_count = 2
    schedule = []
    today = date.today()

    if year and month:
        try:
            request_date = date(int(year), int(month), 1)
        except ValueError:
            request_date = date.today()
    else:
        request_date = date.today()

    request_date = request_date.replace(day=1)
    startMonth = request_date.month

    eventdays = {}
    for day in Post.objects.filter(event_date_start__gte=request_date, event_date_start__lte=request_date + timedelta(60)):
        eventdays.setdefault(day.event_date_start.date(), []).append(day)

    for m in xrange(startMonth, startMonth + months_count):
        if m > 12:
            month = m - 12
            year = request_date.year + 1
        else:
            month = m
            year = request_date.year

        month_days = calendar.monthcalendar(year, month)

        # FIXME: сделать предзагрузку дней тренингов
        for week in month_days:
            for i in xrange(0, len(week)):
                week[i] = {'day': week[i]}
                try:
                    week[i]['date'] = date(year, month, int(week[i]['day']))
                    if today == week[i]['date']:
                        week[i]['today'] = True
                    week[i]['events'] = {'days': eventdays.get(week[i]['date'], []),
                                         }
                except ValueError:
                    week[i]['date'] = ''

        schedule.append({'month': month_days,
                         'number': month,
                         })

    prev_date = (request_date - timedelta(days=15)).replace(day=1)
    next_date = (request_date + timedelta(days=45)).replace(day=1)
    return render_to_response(request, 'schedule.html', {'schedule': schedule,
                                                         'prev_date': prev_date > today - timedelta(days=90) and prev_date or None,
                                                         'prev_link': reverse('schedule_month', args=[prev_date.year, prev_date.month]),
                                                         'next_date': next_date < today + timedelta(days=365) and next_date or None,
                                                         'next_link': reverse('schedule_month', args=[next_date.year, next_date.month]),
                                                         })


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


def user_profile(request, username):
    """ Профиль пользователя """
    domain_user = get_user(username)
    domain_profile = domain_user.get_profile()
    last_comments = Comment.objects.filter(author=domain_user).order_by('-date_created')[:3]
    last_photos = Photo.objects.filter(author=domain_user).order_by('-date_created')[:3]
    page = 'profile'

    return render_to_response(request, 'profile.html', locals())


@auth_only
def my_profile(request):
    """ Профиль пользователя """
    return user_profile(request, request.user)


@auth_only
def drafts(request):
    """ Неопубликованные посты """
    start = parse_timestamp(request.GET.get('start'))
    posts = get_section_objects(request.user, 'draft')
    if start:
        posts = posts.filter(date_created__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
        'title': u"Неопубликованное",
    }

    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].date_created)
        context['posts'] = context['posts'][:10]

    return render_to_response(request, 'my/drafts.html', context)


@auth_only
def my_settings(request):
    u""" Настройки юзера """
    domain_user = request.user
    profile = domain_user.get_profile()
    page = 'settings'
    password_error = ''

    if request.POST.get('action') == 'change_password':
        user = auth.authenticate(username=request.user.username, password=request.POST.get('old_password'))
        if not user:
            password_error = u"Старый пароль неверен"

        if request.POST.get('new_password1') != request.POST.get('new_password2'):
            password_error = u"Новые пароли не совпадают"

        if not password_error:
            user.set_password(request.POST.get('new_password1'))
            user.save()
            password_error = u"Пароль изменен"

    return render_to_response(request, 'my/settings.html', locals())


@posts_feed(template="my/posts.html")
def user_posts(request, username):
    user = get_user(username)

    start = parse_timestamp(request.GET.get('start'))
    posts = get_section_objects(user, 'posts')
    if start:
        posts = posts.filter(date_created__lt=start)

    context = {
        'start': None,
        'posts': posts[:11],
        'title': u"%s: Сообщения" % user.name,
        'domain_user': user,
        'domain_profile': user.get_profile(),
    }

    if len(context['posts']) == 11:
        context['start'] = timestamp(context['posts'][10].date_created)
        context['posts'] = context['posts'][:10]

    return context


def user_staff(request, username, section):
    """ Посты, комментарии, картинки, избранное отдельного юзера """
    user = get_user(username)
    context = {'domain_user': user, 'domain_profile': user.get_profile(), 'page': request.GET.get('page', "")}

    objects = get_section_objects(user, section)

    context.update(make_pages(objects, current_page=context.get('page')))
    context['title'] = user.name + ": " + {
        'comments': u"Комментарии",
        'photos': u"Картинки"
    }.get(section)

    return render_to_response(request, 'my/%s.html' % section, context)


def user_item(request, username, section, item_id):
    """ Пост, картинка юзера """
    user = get_user(username)

    if section == 'posts':
        return user_post(request, user, item_id)
    if section == 'photos':
        return user_photo(request, user, item_id)

    # Остальное пока не реализовано
    raise Http404()


@time_slow
def user_post(request, user, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not (post.status == 'pub' or (request.user.is_authenticated() and post.can_edit(request.user))):
        raise Http404

    profile = user.get_profile()
    context = {'domain_user': user,
               'profile': profile,
               'post': post,
               'can_edit': post.can_edit(request.user),
               'page_identifier': 'post_%s' % post.id,
               }

    return render_to_response(request, 'post.html', context)


@time_slow
def user_photo(request, user, pic_id):
    photo = get_object_or_404(Photo, pk=pic_id, status='pub')
    prev_photo = None
    next_photo = None

    if photo.post:
        try:
            prev_photo = Photo.objects.filter(post=photo.post, pk__lt=photo.pk).order_by('-pk')[0]
        except IndexError:
            prev_photo = None
        try:
            next_photo = Photo.objects.filter(post=photo.post, pk__gt=photo.pk).order_by('pk')[0]
        except IndexError:
            try:
                next_photo = Photo.objects.filter(post=photo.post).exclude(pk=photo.pk).order_by('pk')[0]
            except IndexError:
                pass

    return render_to_response(request, 'photo.html', {'photo': photo,
                                                      'post': photo.post,
                                                      'next_photo': next_photo,
                                                      'prev_photo': prev_photo,
                                                      'can_edit': photo.can_edit(request.user),
                                                      'user': user,
                                                      'page_identifier': 'photo_%s' % photo.id})


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
            print "EDIT"
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.category = form.cleaned_data['category']
            post.geography = form.cleaned_data['geography']
            post.event_date_start = form.cleaned_data['event_date_start']
            post.event_date_finish = form.cleaned_data['event_date_start']

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

                    if post.status == 'pub':
                        new_post_announces.delay(post.id)
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


def edit_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    user = request.user
    if not user:
        raise Http404
    if not photo.can_edit(user):
        raise Http404

    form = None

    if request.POST:
        if request.POST['action'] == u"Сохранить":
            form = PhotoForm(request.POST, photo=photo)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(photo.get_absolute_url())

        elif request.POST['action'] == u"Удалить":
            photo.status = 'del'
            photo.save()

            if photo.post:
                photo.post.content = photo.post.content.replace('<glader pic="%s">' % photo.pk, '')
                photo.post.save()
            return HttpResponseRedirect(user.get_absolute_url())

    else:
        form = PhotoForm(photo=photo)

    return render_to_response(request, 'photo_edit.html', {'form': form, 'photo': photo})


@login_required
def editprofile(request):
    user = request.user
    profile = user.get_profile()
    if request.POST:
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[user.username]))

    else:
        form = ProfileForm(instance=profile)

    return render_to_response(request, 'profile_edit.html', {'form': form, 'domain_user': user})


def editpassword(request):
    pass

###############################################################################
# AJAX


def add_photo(request):
    from django.contrib.sessions.models import Session
    try:
        s = Session.objects.get(pk=request.GET.get('sessionid'))
        user_id = s.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=user_id)
        post = Post.all.get(pk=request.GET.get('post'))

    except (Session.DoesNotExist, User.DoesNotExist, Post.DoesNotExist):
        raise Http404()

    if not post.can_edit(user):
        raise Http404()

    form = PictureForm(request.POST, request.FILES)
    if not form.is_valid():
        raise Http404()

    yafotki_id, url = add_to_yaphoto(form.cleaned_data['Filedata'])
    id = yafotki_id.split(':')[-1]
    image = Photo(author=user, post=post, title='', yandex_fotki_image_src="%s#%s" % (url, id))
    image.save()

    make_thumbnail(image.yandex_fotki_image_src)
    thumbnail_url = get_thumbnail_url(image.yandex_fotki_image_src)

    post.content += ' <glader pic="%s">' % image.pk
    post.save()

    return HttpResponse(simplejson.dumps({
        'success': True,
        'picture_id': image.pk,
        'absolute_url': image.get_absolute_url(),
        'thumbnail_url': settings.STATIC_URL + thumbnail_url
    }))


def add_to_yaphoto(content):
    from core.utils.post_multipart import post_multipart
    content = content.read()

    files = [('image', 'image', content), ]
    status, reason, result = post_multipart(
        settings.YAFOTKI_STORAGE_OPTIONS['host'],
        None,
        settings.YAFOTKI_STORAGE_OPTIONS['post'],
        {},
        files,
        headers={'Authorization': 'OAuth %s' % settings.YAFOTKI_STORAGE_OPTIONS['token']}
    )

    if status != 201:
        raise ValueError("Cannot upload image: %s %s %s (host %s)" % (status, reason, result, settings.YAFOTKI_STORAGE_OPTIONS['host']))

    tree = ET.fromstring(result)
    try:
        id = tree.find('.//{http://www.w3.org/2005/Atom}id').text
        url = tree.find('.//{http://www.w3.org/2005/Atom}content').attrib['src']
        return id, url

    except TypeError:
        raise ValueError('Bad info answer: %s' % result)


@auth_only
def set_name(request):
    user = request.user
    name = sanitizeHTML(request.GET.get('name', ''))
    if not name:
        return JsonErrorResponse(u"Введите желаемое имя")

    reg_form = RegistrationForm()
    if not reg_form.free_credentials(name):
        return JsonErrorResponse(u"Это имя уже занято")

    if len(name) > 30:
        return JsonErrorResponse(u"Слишком длинное имя. Ограничьтесь 30 символами")

    user.first_name = name
    user.save()
    return JsonResponse({'success': True})


@auth_only
def set_news(request):
    user = request.user
    profile = user.get_profile()
    if request.GET.get('news') and request.GET.get('news') != 'false':
        profile.send_news = True
    else:
        profile.send_news = False

    profile.save()
    return JsonResponse({'success': True})


def crossdomain(request):
    return HttpResponse("""<?xml version="1.0"?>
        <!-- http://glader.ru/crossdomain.xml -->
        <cross-domain-policy>
        <allow-access-from domain="%s" />
        </cross-domain-policy>
    """ % settings.DOMAIN)


def tags_suggest(request):
    query = request.GET.get('tag', '')
    tags = [{'caption': t.title, 'value': t.title} for t in Tag.get_by_query(query)]
    if len(query) >= 3 and not {'caption': query, 'value': query} in tags:
        tags.append({'caption': u'+' + query, 'value': query})
    return variants_to_response(tags)


def variants_to_response(variants):
    return HttpResponse(simplejson.dumps(variants, ensure_ascii=False), content_type="application/json; charset=utf-8")


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
