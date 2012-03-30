# -*- coding: utf-8 -*-
import re
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import connection

from django_queue.models import Queue

from core.models import Movie, Man, Tag, Man2Movie, Post
from core.views.common import render_to_response
from core.utils.common import slug


def change_user(request):
    if not request.user.username == 'glader':
        raise Http404()
    username = request.GET.get('user')
    user = User.objects.get(username=username)
    request.session['_auth_user_id'] = user.id
    return HttpResponseRedirect('/')

###############################################################################
# Админка


def moderator_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.get_profile().is_moderator:
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper


@moderator_required
def create_rider(request):
    rider_titles = request.POST['rider']
    object_id = request.POST['object_id']
    movie = Movie.objects.get(pk=object_id)

    for rider_title in rider_titles.split(","):
        rider_name = slug(rider_title)
        try:
            rider = Man.objects.get(slug=rider_name)
            if rider.primary_synonim:
                rider = rider.primary_synonim

        except Man.DoesNotExist:
            rider = Man(slug=rider_name, title=rider_title, is_rider=True, hidden=True)
            rider.save()

        Man2Movie.objects.create(man=rider, movie=movie, role='actor')

    return HttpResponseRedirect('/admind/core/movie/%d/' % movie.pk)


@moderator_required
def create_teaser_announce(request):
    movie = Movie.objects.get(pk=request.GET.get('movie_pk'))

    post = Post.objects.create(title=u'Тизер к фильму "%s"' % movie.title, content='',
                               comment_count=0,
                               status='pub',
                               author=request.user,
                               ip=request.META['REMOTE_ADDR'],
                               type='teaser',
    )

    post.item = movie
    post.best = post.date_created
    post.save()

    Queue.add_task('new_teaser', {"movie_id": movie.id})

    return HttpResponseRedirect('/admind/core/movie/%s/' % request.GET.get('movie_pk'))


@moderator_required
def create_fullmovie_announce(request):
    movie = Movie.objects.get(pk=request.GET.get('movie_pk'))

    post = Post.objects.create(title=u'Выложен фильм "%s"' % movie.title, content='',
                               comment_count=0,
                               status='pub',
                               author=request.user,
                               ip=request.META['REMOTE_ADDR'],
                               type='full_movie',
    )

    post.item = movie
    post.best = post.date_created
    post.save()

    Queue.add_task('new_fullmovie', {"movie_id": movie.id})

    return HttpResponseRedirect('/admind/core/movie/%s/' % request.GET.get('movie_pk'))


@moderator_required
def create_tracklist_announce(request):
    movie = Movie.objects.get(pk=request.GET.get('movie_pk'))

    post = Post.objects.create(title=u'Выложена музыка к фильму "%s"' % movie.title, content='',
                               comment_count=0,
                               status='pub',
                               author=request.user,
                               ip=request.META['REMOTE_ADDR'],
                               type='soundtrack',
    )

    post.item = movie
    post.best = post.date_created
    post.save()

    Queue.add_task('new_tracklist', {"movie_id": movie.id})
    return HttpResponseRedirect('/admind/core/movie/%s/' % request.GET.get('movie_pk'))


@moderator_required
def tag_replace(request):
    new_tag_title = request.POST.get('new_tag')
    object_id = request.POST['object_id']
    if not new_tag_title:
        return HttpResponseRedirect('/admind/core/tag/%s/' % object_id)
    tag = Tag.objects.get(pk=object_id)

    new_tag = Tag.get_tag(new_tag_title)
    if not new_tag:
        new_tag = Tag.objects.create(title=new_tag_title)

    if tag == new_tag:
        return HttpResponse("Tags are the same")

    items = tag.item_set.all()
    for i in items:
        i.tags.remove(tag)
        i.tags.add(new_tag)
    items = tag.photo_set.all()
    for i in items:
        i.tags.remove(tag)
        i.tags.add(new_tag)
    tag.save()
    new_tag.save()

    return HttpResponseRedirect('/admind/core/tag/%s/delete/' % object_id)


@moderator_required
def reports(request):
    if request.GET.get('full'):
        start = date(2008, 9, 1)
    else:
        start = date(2009, 6, 1)

    cursor = connection.cursor()
    cursor.execute("""SELECT d.date, COUNT(p.id)
                        from d
                        left join core_profile p ON d.date=cast(p.date_created as date)
                        WHERE d.date <= '%s' and d.date >= '%s'
                        group by d.date""" % (date.today(), start))
    registrations = cursor.fetchall()

    cursor.execute("""SELECT d.date, COUNT(p.id)
                        from d
                        left join core_item p ON d.date=cast(p.date_created as date) and p.status = 'pub' AND p.type_id=46
                        WHERE d.date <= '%s' AND d.date >= '%s'
                        group by d.date""" % (date.today(), start))
    posts = cursor.fetchall()

    cursor.execute("""SELECT d.date, COUNT(p.id)
                        from d
                        left join core_comment p ON d.date=cast(p.date_created as date)
                        WHERE d.date <= '%s' and d.date >= '%s'
                        group by d.date""" % (date.today(), start))
    comments = cursor.fetchall()

    cursor.execute("""SELECT d.date, COUNT(p.id)
                        from d
                        left join core_itemvote p ON d.date=cast(p.date_created as date)
                        WHERE d.date <= '%s' and d.date >= '%s'
                        group by d.date""" % (date.today(), start))
    votes = cursor.fetchall()

    cursor.execute("""SELECT d.date, COUNT(p.id)
                        from d
                        left join core_item p ON d.date=cast(p.date_created as date) AND p.status = 'pub' AND p.type_id=46
                        WHERE d.date <= '%s' and d.date >= '%s'
                        AND abstract='LAhmatyi'
                        group by d.date""" % (date.today(), start))
    content = cursor.fetchall()

    cursor.execute("""SELECT d.date, COUNT(p.id)
                        from d
                        left join core_item p ON d.date=cast(p.date_created as date)
                            AND p.type_id=46 AND p.status = 'pub'
                            AND (p.abstract is null or p.abstract != 'LAhmatyi') and p.author_id != 1
                        WHERE d.date <= '%s' and d.date >= '2009-10-01'
                        group by d.date""" % date.today())
    good_posts = cursor.fetchall()

    return render_to_response(request, 'reports.html', locals())


@moderator_required
def memcache_report(request):
    try:
        import memcache
    except ImportError:
        raise Http404

    if not request.user.get_profile().is_moderator:
        raise Http404

    # get first memcached URI
    m = re.match(
        "memcached://([.\w]+:\d+)", settings.CACHE_BACKEND
    )
    if not m:
        raise Http404

    host = memcache._Host(m.group(1))
    host.connect()
    host.send_cmd("stats")

    class Stats:
        pass

    stats = Stats()

    while 1:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = timedelta(seconds=value)
            elif key == "time":
                value = datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()

    return render_to_response(
        request,
        'reports_memcached.html', dict(
            stats=stats,
            hit_rate=100 * stats.get_hits / stats.cmd_get,
            time=datetime.now(),  # server time
        ))


@moderator_required
def observe_404(request):
    u""" Страница с просмотром последних 404 """
    exceptions = set()
    links = {}
    for l in open(settings.ACCESSLOG_PATH):
        row = l.strip().split(' ', 11)
        record = {}
        for i, field in enumerate(('ip', 'host', '_', 'dt', 'tz', 'method', 'url', 'protocol', 'answer', 'size', 'referrer', 'ua')):
            record[field] = row[i]
        record['dt'] = record['dt'][1:]

        if record['answer'] != '404':
            continue
        for ex in exceptions:
            if ex in record['url']:
                continue

        links.setdefault(record['url'], []).append(record)

    unique_links = [(i, url, links[url][-1]['dt'], reversed(links[url])) for i, url in enumerate(links)]
    unique_links.sort(key=lambda rec: rec[2], reverse=True)

    return render_to_response(request, 'admin/observe_404.html', {'links': unique_links})


def human_timedelta(t):
    sec = t / 1000000
    rem = t % 1000000
    return "%d.%06d" % (sec, rem)


@moderator_required
def timing_report(request):
    u""" Страница с просмотром хронометража проекта """
    links = {}
    measures = []
    for l in open(settings.LOGGING['handlers']['search']['filename']):
        row = l.strip().split('\t')
        row[0] = int(re.sub('[^\d]', '', row[0]))
        links.setdefault(row[1], []).append(row[0])

    for i, url in enumerate(links):
        links[url].sort(reverse=True)

        measures.append({'id': i,
                          'url': url,
                          'amount': len(links[url]),
                          'average': human_timedelta(sum(links[url]) / len(links[url])),
                          'min': human_timedelta(links[url][-1]),
                          'max': human_timedelta(links[url][0]),
                          'all': [human_timedelta(t) for t in links[url]],
})

    measures.sort(key=lambda r: r['average'], reverse=True)

    return render_to_response(request, 'admin/timing_report.html', {'links': measures[: 60]})
