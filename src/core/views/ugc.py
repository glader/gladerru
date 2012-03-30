# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from itertools import groupby
import calendar
import re
from xml.etree import ElementTree as ET

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.utils import simplejson

from django_queue.models import Queue

from core.forms import PostForm, LoginForm, RegistrationForm, ProfileForm, AvatarForm, PictureForm, \
    PhotoForm, PostCommentForm, PostVoteForm, CommentVoteForm, CommentForm, sanitizeHTML
from core.models import Post, Friend, UserNews, ItemVote, Movie, Photo, Comment, Profile, Tag, News, \
    Keyword, PictureBox, TagsCloud
from core.signals import new_comment_signal
from core.templatetags.content import link, good_or_bad, signed_number, decimal_cut, \
    make_pages, make_tag_pages, get_avatar_url, thumbnail
from core.utils.common import process_template, send_html_mail
from core.views.common import render_to_response
from core.decorators import time_slow, auth_only, posts_feed
from core.utils.thumbnails import get_thumbnail_url, make_thumbnail


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

@time_slow
@posts_feed(template="index.html")
def index(request):
    return best_posts(request.GET.get('page'))


@time_slow
def tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    if tag.primary_synonim:
        return HttpResponsePermanentRedirect(tag.primary_synonim.get_absolute_url())

    filter = request.GET.get('filter', '')
    if filter not in ('best', 'userphoto'):
        filter = ''
    context = {'page': request.GET.get('page', ""),
               'tag': tag,
               'filter': filter,
               'filters': [{'code':'best', 'title':u'Лучшие посты'},
                           {'code':'', 'title':u'Все посты'},
                           {'code':'userphoto', 'title':u'Фотографии'}, ]
               }

    if filter == 'best':
        item_ids = [int(id) for id in tag.posts.split(',')] if tag.posts else []
        items = Post.objects.filter(pk__in=item_ids, hidden=False, best__isnull=False).order_by('-date_created')
        context.update(make_pages(items, current_page=context.get('page')))

    elif filter == 'userphoto':
        items = tag.photo_set.filter(status='pub').order_by('-date_created')
        context.update(make_pages(items, current_page=context.get('page')))

    else:
        context.update(make_tag_pages(tag, current_page=context.get('page')))

    template = filter == 'userphoto' and 'tag_photos.html' or 'tag.html'
    return render_to_response(request, template, context)


def tags(request):
    tags = Tag.objects.filter(size__gt=1, type__gt=10).order_by('title')
    tags_cloud = TagsCloud(tags)
    tags_cloud.set_rel_sizes(12, 30)
    return render_to_response(request, 'tags_all.html', {'tags': tags})


def messages_compose(request):
    from messages.views import compose
    recipient = None
    if request.method == 'GET' and request.GET.get('recipient'):
        recipient = request.GET.get('recipient')
    return compose(request, recipient=recipient)

###############################################################################
# UGC
###############################################################################


@time_slow
@posts_feed()
def all(request):
    """ Свежие записи во всех блогах """
    context = {'page': request.GET.get('page', ""),
               'title': u'Все сообщения',
               'menu_item': 'all_posts',
               }
    context.update(make_pages(Post.objects.filter(status='pub').order_by('-date_created'), current_page=context.get('page')))
    return context


@auth_only
@posts_feed()
def hidden(request):
    """ Вообще все посты, для модераторов """
    if not request.user.get_profile().is_moderator:
        raise Http404
    context = {'page': request.GET.get('page', ""),
               'title': u'Все сообщения',
               'menu_item': 'all_posts',
               }
    context.update(make_pages(Post.objects.all().order_by('-date_created'), 30, context.get('page')))
    return context


@time_slow
@posts_feed()
def top_rating(request):
    u""" Лучшие за месяц """
    items = Post.objects \
                .filter(date_created__gte=date.today() - timedelta(days=30)) \
                .order_by('-rating')[:10]
    return {'items': items, 'title': u'Лучшие за месяц', 'menu_item': 'rating'}


@time_slow
@posts_feed()
def top_discussed(request):
    u""" Самые обсуждаемые за месяц """
    items = Post.objects \
                .filter(date_created__gte=date.today() - timedelta(days=30), comment_count__gt=0) \
                .order_by('-comment_count')[:10]
    return {'items': items, 'title': u'Самые обсуждаемые за месяц', 'menu_item': 'discussed'}


@time_slow
def users_best(request):
    profiles = Profile.objects.all().order_by('-rating')[:20]
    title = u"Лучшие посетители"
    menu = 'users_best'
    return render_to_response(request, 'top_users.html', locals())


@time_slow
def users_new(request):
    profiles = Profile.objects.all().order_by('-date_created')[:20]
    title = u"Youngblood"
    menu = 'users_new'
    return render_to_response(request, 'top_users.html', locals())


@posts_feed(template="faq.html")
def faq(request):
    u""" Посты с пометкой 'Вопрос' """
    context = {'page': request.GET.get('page', ""), }
    context.update(make_pages(Post.objects.filter(tags__name='question').order_by('-date_created'), current_page=context.get('page')))
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
        objects = Post.all.filter(author=user, status__in=('save', 'deferred')) \
                    .order_by('-date_created')

    elif section == 'comments':
        objects = Comment.objects.filter(author=user).order_by('-date_created')

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
    if request.user and request.user.is_authenticated() and not domain_user == request.user:
        my_friend = bool(Friend.objects.filter(user_a=request.user, user_b=domain_user).count())
    return render_to_response(request, 'profile.html', locals())


def user_friends(request, username):
    u""" Друзья юзера """
    domain_user = get_user(username)
    friends = Friend.objects.filter(user_a=domain_user).select_related('subject')
    page = 'friends'
    return render_to_response(request, 'my/friends.html', locals())


@auth_only
def my_profile(request):
    """ Профиль пользователя """
    return user_profile(request, request.user)


@auth_only
def my_friends(request):
    u""" Друзья юзера """
    domain_user = request.user
    friends = Friend.objects.filter(user_a=domain_user).select_related('subject')
    page = 'friends'
    return render_to_response(request, 'my/friends.html', locals())


def get_user_news(user):
    usernews = UserNews.objects.filter(user=user)
    news = list(News.objects.filter(pk__in=[n.news_id for n in usernews]))
    news.sort(key=lambda n: n.date_created, reverse=True)
    news = [{'date': k, 'news': list(v)} for k, v in groupby(news, key=lambda n:n.date_created.date())]
    return news


@auth_only
def my_news(request):
    u""" Новости юзера """
    domain_user = request.user
    page = 'news'
    news = get_user_news(domain_user)

    profile = domain_user.get_profile()
    profile.unread_news_count = 0
    profile.save()
    return render_to_response(request, 'my/news.html', locals())


@auth_only
def drafts(request):
    """ Неопубликованные посты """
    context = {'title': u"Неопубликованное"}
    objects = get_section_objects(request.user, 'draft')
    context.update(make_pages(objects, current_page=context.get('page')))
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
    context = {'domain_user': user,
               'domain_profile': user.get_profile(),
               'page': request.GET.get('page', ""),
               'title': u"%s: Сообщения" % user.name,
               }

    objects = get_section_objects(user, 'posts')
    context.update(make_pages(objects, current_page=context.get('page')))
    return context


def user_staff(request, username, section):
    """ Посты, комментарии, картинки, избранное отдельного юзера """
    user = get_user(username)
    context = {'domain_user': user, 'domain_profile': user.get_profile(), 'page': request.GET.get('page', "")}

    objects = get_section_objects(user, section)
    context.update(make_pages(objects, current_page=context.get('page')))
    context['title'] = user.name + ": " + \
                        {'comments': u"Комментарии",
                        'photos': u"Картинки"}.get(section)
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
               'can_edit': post.can_edit(request.user)
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
                                                      'user': user})


@auth_only
def commented(request):
    # TODO: складывать новые комментарии в новости отдельного типа
    return render_to_response(request, 'my/commented.html', {'items': []})


@login_required
def offer_movie(request):
    """ Формирование поста с новым фильмом """
    post = template_post("offer_movie.html",
                         {},
                         u"Фильмы",
                         request.user,
                         request.META['REMOTE_ADDR'])
    return HttpResponseRedirect(reverse('edit_post', args=[post.id]))


@login_required
def offer_rider(request):
    """ Формирование поста с новым райдером """
    post = template_post("offer_rider.html",
                         {},
                         u"Разное, Райдеры",
                         request.user,
                         request.META['REMOTE_ADDR'])
    return HttpResponseRedirect(reverse('edit_post', args=[post.id]))


@login_required
def offer_moviemaker(request):
    """ Формирование поста с новой студией """
    post = template_post("offer_moviemaker.html",
                         {},
                         u"Фильмы, Студии",
                         request.user,
                         request.META['REMOTE_ADDR'])
    return HttpResponseRedirect(reverse('edit_post', args=[post.id]))


def template_post(template, context, tags, author, ip):
    title, content = process_template('posts/%s' % template, context)
    post = Post(title=title, content=content, comment_count=0, status='save', author=author, ip=ip)
    post.save()

    for tag in Tag.process_tags(tags):
        post.tags.add(tag)
    post.rebuild_tags()
    return post


def process_keywords(post):
    u"""Заменяет слова на ссылки по таблице Keywords"""
    words = list(Keyword.objects.all())
    words.sort(key=lambda word: len(word.keyword), reverse=True)
    for word in words:
        if word.keyword in post.content:
            content = re.sub(u'(<[^>]+)%s' % word.keyword, lambda res: res.group(1) + u'ЪЪЪЪЪ', post.content, re.I)
            content = re.sub(u'(?<!>)%s(?!<)' % word.keyword,
                                  u'<a href="%s" title="ЪЪЪЪЪ">%s</a>' % (word.url, word.keyword),
                                  content,
                                  1)
            content = re.sub(u'(?<!>)%s(?!<)' % word.keyword,
                                  u'<span>%s</span>' % word.keyword,
                                  content)
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
            post.geography = form.cleaned_data['geography']
            post.event_date_start = form.cleaned_data['event_date_start']
            post.event_date_finish = form.cleaned_data['event_date_start']

            process_keywords(post)

            # Теги
            post.tags.clear()
            post.tags.add(*form.cleaned_data['tags'])

            video_tag = Tag.objects.get(name='video')
            if ('<youtube' in post.content or '<embed' in post.content) and \
                not video_tag in form.cleaned_data['tags']:
                    post.tags.add(video_tag)

            # Статус
            status = {u'Удалить': 'del', u'Опубликовать': 'pub', u'В черновики': 'save'} \
                    .get(request.POST['action'])
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
                        Queue.add_task('new_post', {"post_id": post.id})
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


@login_required
def editavatar(request):
    user = request.user
    if request.POST or request.FILES:
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user)
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = AvatarForm(initial={})

    return render_to_response(request, 'avatar_edit.html', {'form': form, 'domain_user': user})


def editpassword(request):
    pass

###############################################################################
# AJAX


def add_comment(request, user=None, hidden=False):
    if not user:
        user = request.user

    if isinstance(user, AnonymousUser):
        # TODO: log this
        raise Http404

    form = PostCommentForm(request.GET, user=user)
    if form.is_valid():
        if form.cleaned_data['comment']:
            comment = form.cleaned_data['comment']
            last_answers = form.cleaned_data['post'].comments.\
                                extra(where=['LENGTH(`order`) = %s' % (len(comment.order) + 3),
                                             '`order` LIKE "%s%%%%"' % comment.order]).\
                                order_by('-order')

        elif form.cleaned_data['post']:
            last_answers = form.cleaned_data['post'].comments.\
                                extra(where=['LENGTH(`order`) = 3']).order_by('-order')

        else:
            raise IndexError()

        answer_on = form.cleaned_data['comment'] or form.cleaned_data['post']
        if last_answers:
            def get_next_number(order, digits=3):
                next = str(int(order) + 1)
                return '0' * (digits - len(next)) + next

            curr_order = last_answers[0].order
            curr_order = re.sub('(\d{3})$', lambda res: get_next_number(res.group(1)), curr_order)
        else:
            curr_order = form.cleaned_data['comment'] and (form.cleaned_data['comment'].order + '001') or '001'

        # place
        try:
            last_inherit = form.cleaned_data['post'].comments\
                            .filter(order__startswith=(form.cleaned_data['comment'] and form.cleaned_data['comment'].order or ''))\
                            .order_by('-order')[0]
            comment_place = last_inherit.pk
        except IndexError:
            if form.cleaned_data['comment']:
                comment_place = form.cleaned_data['comment'].pk
            else:
                comment_place = ''

        comment = Comment(item=form.cleaned_data['post'],
                          content=form.cleaned_data['content'],
                          order=curr_order,
                          author=user,
                          status='pub',
                          hidden=hidden,
                          ip=request.META['REMOTE_ADDR'],
                          )
        comment.save()

        form.cleaned_data['post'].comment_count = (form.cleaned_data['post'].comment_count or 0) + 1
        form.cleaned_data['post'].last_comment_date = comment.date_created
        form.cleaned_data['post'].save()

        profile = user.get_profile()
        profile.comment_count += 1
        profile.save()

        new_comment_signal.send(sender=comment, post=form.cleaned_data['post'], answer_on=answer_on, author=user)

        comment.author = user
        comment.profile = profile
        comment.avatar = get_avatar_url(profile, 32)
        comment.profile_link = link(user)

        template = loader.get_template("blocks/b-comment.html")
        html = template.render(Context({'comment': comment,
                                        'post': form.cleaned_data['post'],
                                        'MEDIA_URL': settings.MEDIA_URL,
                                        'klass': form.cleaned_data['post'].__class__.__name__.lower()
                                        }))

        result = {'success': True,
                  'html': html,
                  'afterComment': comment_place
                  }

    else:
        if 'retpath' in request.GET:
            return HttpResponseRedirect(request.GET['retpath'])
        else:
            return JsonErrorResponse(form.str_errors())

    if 'retpath' in request.GET:
        return HttpResponseRedirect(request.GET['retpath'])

    return HttpResponse(simplejson.dumps(result))


def vk_comment(request):
    user = User.objects.get(username='vkontakte')
    send_html_mail(
        'Glader.ru: new vk comment',
        u"New comment: '%s' on item '%s_%s'" % (request.GET.get('content'),
                                                 request.GET.get('klass'),
                                                 request.GET.get('post')),
        'glader.ru@gmail.com'
    )

    return add_comment(request, user=user, hidden=True)


@auth_only
def add_post_vote(request):
    user = request.user
    form = PostVoteForm(request.GET, user=user)
    if form.is_valid():
        post = form.cleaned_data['post']
        add_vote(post, user, request.META['REMOTE_ADDR'])
        template_filter = isinstance(post, Movie) and decimal_cut or signed_number
        result = {'success': True,
                  'vote_class': 'rating_' + good_or_bad(post.rating),
                  'rating': str(template_filter(post.rating))
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
        Queue.add_task('best_post', {"post_id": post.id, "klass": post.__class__.__name__})

    post.save()


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

    return HttpResponse(simplejson.dumps({'success': True,
                                           'picture_id': image.pk,
                                           'absolute_url': image.get_absolute_url(),
                                           'thumbnail_url': settings.MEDIA_URL + thumbnail_url
                                           }))


def add_to_yaphoto(content):
    from core.utils.post_multipart import post_multipart
    content = content.read()

    files = [('image', 'image', content), ]
    status, reason, result = post_multipart(settings.YAPHOTO_HOST,
                                            None,
                                            settings.YAPHOTO_POST,
                                            {},
                                            files,
                                            headers={'Authorization': 'OAuth %s' % settings.YAPHOTO_TOKEN}
    )

    if status != 201:
        raise ValueError("Cannot upload image: %s %s %s (host %s)" % (status, reason, result, settings.YAPHOTO_HOST))

    tree = ET.fromstring(result)
    try:
        id = tree.find('.//{http://www.w3.org/2005/Atom}id').text
        url = tree.find('.//{http://www.w3.org/2005/Atom}content').attrib['src']
        return id, url

    except TypeError:
        raise ValueError('Bad info answer: %s' % result)


@auth_only
def best_answer(request):
    user = request.user
    form = CommentForm(request.GET)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        post = comment.item
        if not post.can_edit(user):
            raise Http404

        if request.GET.get('del'):
            post.best_answer = None
        else:
            post.best_answer = comment
        post.save()

        result = {'success': True}
    else:
        if 'retpath' in request.GET:
            return HttpResponseRedirect(request.GET['retpath'])
        else:
            return JsonErrorResponse(form.str_errors())

    if 'retpath' in request.GET:
        return HttpResponseRedirect(request.GET['retpath'])
    else:
        return JsonResponse(result)


@auth_only
def add_friend(request):
    user = request.user
    try:
        new_friend = User.objects.get(username=request.GET.get('user'))
    except User.DoesNotExist:
        return JsonErrorResponse(u"Вы пытаетесь подружиться с несуществующим пользователем")

    if Friend.objects.filter(user_a=user, user_b=new_friend).count():
        return JsonErrorResponse(u"Вы уже дружите с этим пользователем")

    Friend.objects.create(user_a=user, user_b=new_friend)
    Queue.add_task('new_friend', {"user": user.id, "new_friend": new_friend.id})
    return JsonResponse({'success': True})


@auth_only
def cancel_friend(request):
    user = request.user
    try:
        new_friend = User.objects.get(username=request.GET.get('user'))
    except User.DoesNotExist:
        return JsonErrorResponse(u"Вы прекратить дружбу с несуществующим пользователем")

    if not Friend.objects.filter(user_a=user, user_b=new_friend).count():
        return JsonErrorResponse(u"Вы и так не дружите с этим пользователем")

    Friend.objects.filter(user_a=user, user_b=new_friend).delete()
    return JsonResponse({'success': True})


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
    """ % settings.MEDIA_DOMAIN)


def tags_suggest(request):
    query = request.GET.get('tag', '')
    tags = [{'caption':t.title, 'value':t.title} for t in Tag.get_by_query(query)]
    if len(query) >= 3 and not {'caption': query, 'value': query} in tags:
        tags.append({'caption': u'+' + query, 'value': query})
    return variants_to_response(tags)


def variants_to_response(variants):
    return HttpResponse(simplejson.dumps(variants, ensure_ascii=False), content_type="application/json; charset=utf-8")


def picturebox(request):
    picture = get_object_or_404(Photo, pk=request.GET.get('picture_id'))
    user = request.user.is_authenticated() and request.user or None
    record = PictureBox(user=user, picture=picture, action=request.GET.get('action'))
    record.save()
    if request.GET.get('action') == 'good':
        result = {}
    else:
        next_picture = PictureBox.get_next_picture(user)
        result = {'success': True, 'picture_id': next_picture.pk, 'preview': link(next_picture)}
    return JsonResponse(result)


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
