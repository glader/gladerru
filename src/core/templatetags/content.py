# encoding: utf-8

from datetime import datetime
import re
import urllib
from urllib import quote

from django import template
from django.template import Context, loader, TemplateDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.core.paginator import QuerySetPaginator
from django.contrib.auth.models import User
from django.conf import settings

from core.models import Post, Mountain, Region, PictureBox, Photo, Word, Man, Tag, \
    Comment, Song, Movie, Studio, Profile, Avatar
from core.utils.common import cached
from core.utils.log import get_logger
from core.decorators import time_slow
from core.views.common import render_to_string
from core.utils.thumbnails import get_thumbnail_url

register = template.Library()


@register.simple_tag
def DOMAIN():
    return settings.DOMAIN


@register.simple_tag
def MEDIA_URL():
    return settings.MEDIA_URL


@register.simple_tag
def VK_API_ID():
    return settings.VK_API_ID


@register.simple_tag
def get_params(request, param1, value1, param2=None, value2=None):
    """ Строит query строку, добавляя переданные параметры """
    params = dict(request.GET)
    for k, v in params.iteritems():
        if isinstance(v, list):
            params[k] = v[0]
    params[param1] = value1
    if param2:
        params[param2] = value2
    return "&".join("%s=%s" % (k, urllib.quote(v)) for k, v in params.iteritems())


def make_pages(querySet, items_at_page=20, current_page=None):
    pages = QuerySetPaginator(querySet, items_at_page)

    page_number = validate_page_number(current_page, pages.num_pages)
    posts = pages.page(page_number).object_list
    context = {'items': posts}
    avatars = Avatar.get([post.author_id for post in posts], 32)
    for post in posts:
        post.avatar = avatars[post.author_id]
    context.update(other_pages(page_number, pages.num_pages))
    return context


def make_tag_pages(tag, items_at_page=20, current_page=None):
    item_ids = [int(id) for id in tag.posts.split(',')] if tag.posts else []
    num_pages = (len(item_ids) + items_at_page - 1) / items_at_page
    page_number = validate_page_number(current_page, num_pages)

    page_ids = item_ids[(page_number - 1) * items_at_page:page_number * items_at_page]
    posts = list(Post.objects.filter(hidden=False, id__in=page_ids))
    posts.sort(key=lambda p: p.date_created, reverse=True)
    context = {'items': posts}

    avatars = Avatar.get([post.author_id for post in posts], 32)
    for post in posts:
        post.avatar = avatars[post.author_id]

    context.update(other_pages(page_number, num_pages))
    return context


def get_mountains(region=None):
    if region:
        regions = [region]
        mountains = Mountain.objects.filter(region=region)
    else:
        regions = Region.objects.all()
        mountains = Mountain.objects.all()

    regions_dict = dict((r.id, r) for r in regions)
    for m in mountains:
        if not hasattr(regions_dict[m.region_id], 'mountains'):
            regions_dict[m.region_id].mountains = []
        regions_dict[m.region_id].mountains.append(m)

    return {'regions': regions, 'mountains': mountains}


def validate_page_number(page, total):
    if page:
        try:
            page = int(page)
            if 1 <= page <= total:
                return page
        except ValueError:
            pass

    return 1


def other_pages(page, total):
    return {
               'pages': range(1, total + 1),
               'showed_pages': [p for p in range(1, total + 1) if abs(p - page) <= 4],
               'page_number': page,
               'first_page': page != 1 and 1 or None,
               'prev_page': page != 1 and page - 1 or None,
               'next_page': page != total and page + 1 or None,
               'last_page': page != total and total or None,
               }


@register.inclusion_tag("block_hierarchy.html")
def hierarchy(item):
    parents = [{'title':item.title}]
    i = 0
    while i < 100:
        p = item.get_parent()
        if p:
            item = p
            parents.append({'title': item.title, 'link': item.get_absolute_url()})
        else:
            break
        i += 1
    if i > 90:
        raise IndexError(u"Что-то не так с иерархией, глубина вложенности - %s" % i)

    parents.reverse()
    return {'links': parents}


@register.inclusion_tag("block_top_menu.html")
def top_menu(level2='best', level1=None):
    submenu = {'posts': [
                        ['new', '/post/new', u'написать', u'Все ждут от тебя новый пост'],
                        ['best', '/', u'лучшие', u'Сообщения, выбранные читателями'],
                        ['all_posts', '/all', u'новые', u'Голосуй за лучшее'],
                        #['schedule', '/schedule', u'календарь', u'События по датам'],
                        ['rating', '/top/best', u'рейтинг', u'Самые лучшие за месяц'],
                        ['discussed', '/top/comments', u'обсуждаемые', u'Самые обсуждаемые за месяц'],
                        ],
                'users': [
                        ['users_best', '/rating/users/best', u'лучшие', u'доска почета'],
                        ['users_new', '/rating/users/new', u'новые', u'youngblood'],
                        ],
                'articles': [
                        ['newbie', '/skills/newbie', u'новичку', u'как начать кататься на сноуборде и что для этого нужно'],
                        ['beginner', '/skills/beginner', u'опытным райдерам', u'тонкости и интересные моменты сноубординга'],
                        ['freestyle', '/skills/freestyle', u'фристайл', u'те, кто хочет прыгать с трамплинов'],
                        ['freeride', '/skills/freeride', u'фрирайд', u'тем, кто хочет катать в больших горах'],
                        ['jibbing', '/skills/jibbing', u'джиббинг', u'тем, кто хочет слайдить по перилам'],
                        ['carving', '/skills/carving', u'карвинг', u'тем, кто хочет резать дуги'],
                        ],
                'movies': [
                        ['2011', '/movies?page=2011', u'2011', u'Фильмы 2011 года'],
                        ['2010', '/movies?page=2010', u'2010', u'Фильмы 2010 года'],
                        ['2009', '/movies?page=2009', u'2009', u'Фильмы 2009 года'],
                        ['all', '/movies?page=all', u'все', u'Все фильмы'],
                        ['teasers', '/movies/teasers', u'тизеры', u'Тизеры к фильмам'],
                        ['soundtracks', '/movies/soundtracks', u'саундтреки', u'Музыкальные треки к фильмам'],
                        ['studies', '/studies', u'студии', u'Авторы фильмов'],
                        ],
                'mountains': [
                        ['map', '/mountains', u'карта', u'Горки: информация, фотографии, цены, отзывы.'],
                        ],
                'reference': [
                        ['people', '/people', u'люди', u'Райдеры, фотографы и прочие'],
                        ['dictionary', '/terms', u'словарь', u'Словарь всяких терминов'],
                        #['companies', '/content/companies.htm', u'фирмы', u'производители оборудования'],
                        ],
                'profile': [
                        ['messages', '/messages/inbox/', u'сообщения', u'Личные сообщения'],
                        ['friends', '/my/friends', u'друзья', u'Список моих друзей'],
                        ['news', '/my/news', u'новости', u'Анонсы событий, интересных мне'],
                        ['commented', '/my/commented', u'комментарии', u'Новые комментарии к постам, за которыми вы следите'],
                        ['drafts', '/my/drafts', u'черновики', u'начатое и неоконченное'],
                        ['settings', '/my/settings', u'настройки', u''],
                        ]
               }

    def find_levels(level1, level2):
        if level1:
            return level1, level2

        if level2 in submenu:
            return level2, None

        for l1 in submenu.keys():
            for l2 in submenu[l1]:
                if l2[0] == level2:
                    return l1, level2

        return None, None

    level1, level2 = find_levels(level1, level2)

    return {'level1': level1, 'level2': level2, 'submenu': level1 and submenu[level1] or []}


@register.inclusion_tag("block_dop_menu.html")
def dop_menu(type):
    if not type:
        return {'items': []}
    title = {'movie_menu': u'Фильмы', 'articles_menu': u'Статьи', 'world_menu': u'Мир'}.get(type, "").upper()
    return {'items': Post.objects.filter(rubric__name=type), 'title': title}


@register.inclusion_tag("blocks/b-picturebox.html")
def picturebox(user):
    u"""Случайная картинка для оценки"""
    return {'picture': PictureBox.get_next_picture(user)}


@register.filter
def post_cut(post):
    if not post.content:
        return ""
    #FIXME: заменить на парсинг через BeatifulSoap
    result = re.search(u"<cut(?:\s+text=['\"]([^'\"]+)['\"])?>", post.content)

    if result:
        content = post.content[:result.start()] + u'<a href="%s">%s</a>' % (post.get_absolute_url(),
                                                                        result.group(1) or u"Читать далее »")
    else:
        content = post.content

    return mark_safe(content)


@register.filter
def first_paragraph(item):
    if not item.content:
        return ""
    return item.content.split("\n")[0] + u'<a href="%s">%s</a>' % (item.get_absolute_url(), u"Читать далее »")


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


@register.filter
def type_name(item):
    u"""Имя для иконки в поиске"""
    if isinstance(item, Post):
        if item.name:
            return 'article'
        else:
            return 'post'
    return item.__class__.__name__.lower()


@register.inclusion_tag('block_pagination.html', takes_context=True)
def pagination(context, url=""):
    if not url:
        url = context['request'].get_full_path()
    context['url'] = re.sub('&?page=[^&]+', '', url)
    return context


@register.filter
def add_page(url, page):
    if page > 1:
        if '?' in url:
            url += '&'
        else:
            url += '?'
        return url + 'page=%s' % page
    else:
        return url


@register.inclusion_tag('block_riders.html')
def riders(movie):
    riders = Man.objects.filter(man2movie__movie=movie, man2movie__role='actor').order_by('title')
    return {'riders': riders}

##########################################################


@register.filter
def linebreaks(text):
    if not text:
        return ""
    return re.sub('\r?\n', '<br/>\n', text)


@register.filter
def parser(text):
    if not text:
        return ""

    def tagsParser(result):
        if ' ' in result.group(1):
            tag, tokens = result.group(1).split(' ', 1)
        else:
            tag, tokens = result.group(1), ""
        params = dict((p, v) for p, v in re.findall('(\w+)=[\'\"]([^\'\"]+)[\'\"]', tokens))
        item = None
        if 'item' in params:
            if tag == 'ImageLink':
                try:
                    item = Photo.objects.get(slug=params['item'])
                except Photo.DoesNotExist:
                    open('/var/log/projects/gladerru/miss', 'a').write((u"[неизвестная картинка %s in fragment '%s']\n" % (params['item'], result.group(1))).encode('utf8'))
                    return ""
            else:
                for model, field in ((Post, 'name'), (Movie, 'slug'), (Word, 'slug'), (Man, 'slug'), (Mountain, 'name'), (Studio, 'slug')):
                    try:
                        item = model.objects.get(**{field: params['item']})
                    except model.DoesNotExist:
                        pass

                if not item:
                    log = get_logger('miss')
                    log.error(u"Неизвестная страница %s in fragment '%s'", params['item'], result.group(1))
                    return ""

        if not tag:
            return ""
        if tag == "Pre":
            return "<pre>"
        if tag == "EndPre":
            return "</pre>"
        if tag == 'ImageLink':
            return '<a href="%s" style="%s"><img class="userphoto" src="%s%s"></a>' \
                    % (item.get_absolute_url(), params.get('style', ""), settings.MEDIA_URL, thumbnail(item.yandex_fotki_image_src))
        if tag == 'ItemLink':
            return '<a href="%s" style="%s">%s</a>' \
                    % (item and item.get_absolute_url() or "", params.get('style', ""), params.get('title', item and item.title or ""))

    def usernameParser(result):
        username = result.group(1)
        try:
            user = User.objects.get(username=username)
            return "<a href='http://%s.glader.ru/' class='profile_link_default'>%s</a>" % (username, user.name)
        except User.DoesNotExist:
            return u"[неизвестный пользователь]"

    def smiles(result):
        return '<span class="smile">%s</span>' % result.group(1)

    def headers(result):
        number = int(len(result.group(2))) + 1
        return "<h%s>%s</h%s>" % (number, result.group(3), number)

    def pictureParser(result):
        try:
            picture = Photo.objects.get(pk=int(result.group(1)))
        except (Photo.DoesNotExist, ValueError):
            try:
                picture = Photo.objects.get(slug=result.group(1))
            except (Photo.DoesNotExist, ValueError):
                return u""

        return '<a href="%s"><img class="userphoto" src="%s%s"></a>&#32;' % \
               (picture.get_absolute_url(), settings.MEDIA_URL, thumbnail(picture.yandex_fotki_image_src))

    def pageParser(result):
        try:
            page = Post.objects.get(name=result.group(1))
            return link(page)
        except Post.DoesNotExist:
            return u"[Страница с таким кодом не найдена]"

    def userParser(result):
        try:
            user = User.objects.get(username=result.group(1))
            return link(user)
        except User.DoesNotExist:
            return u"[Юзер с таким кодом не найден]"

    def rutubeId(result):
        return """<script>
            rt_mode = "movie";
            rt_movie_id = "%s";
            function rt_show_movie(t){
                document.write(t.playerCode);
            }
            </script>
            <script src="http://rutube.ru/js/api.js"></script>""" % result.group(1)

    def youtubeLink(result):
        try:
            url = "/%s/%s" % (result.group(1), result.group(2))
        except IndexError:
            url = "/v/%s&rel=1" % result.group(1)

        return """<object width="425" height="350">
            <param name="movie" value="http://www.youtube.com%s"></param>
            <param name="wmode" value="transparent"></param>
            <embed src="http://www.youtube.com/%s" type="application/x-shockwave-flash" wmode="transparent"
            width="425" height="350"></embed></object> """ \
                % (url, url)

    def rutubeLink(result):
        return """<OBJECT width="400" height="353">
            <PARAM name="movie" value="http://video.rutube.ru/%s" />
            <PARAM name="wmode" value="window" />
            <PARAM name="allowFullScreen" value="true"></PARAM>
            <EMBED src="http://video.rutube.ru/%s" type="application/x-shockwave-flash"
            wmode="window" width="400" height="353" allowFullScreen="true"/></OBJECT>""" \
               % (result.group(1), result.group(1))

    def emailHider(result):
        email = result.group(1)
        message = "<script>\n" \
                + "".join("document.write('%s');\n" % email[i:i + 4] for i in xrange(0, len(email), 4)) \
                + "</script>\n" \
                + u"<noscript>[Email скрыт от роботов. Включите javascript, чтобы увидеть его.]</noscript>"
        return message

    text = re.sub('(?<!</(td|tr|le|li|ol|ul))\r?\n', '<br/>\n', text)
    text = re.sub('<:(.+?):>', tagsParser, text)
    text = re.sub('<~(\w+)>', usernameParser, text)
    text = re.sub('''<glader\s+pic=['"](\d+)["']>''', pictureParser, text)
    text = re.sub('''<glader\s+page=['"]([^"']+)['"]>''', pageParser, text)
    text = re.sub('''<glader\s+user=['"]([^"']+)['"]>''', userParser, text)
    text = re.sub('(^|\n)(=+)([^\r\n]+)[\r\n]+', headers, text)

    text = re.sub('([\w\d\._-]+@[\w\d\._-]+)', emailHider, text)

    #FIXME: заменить на один тег movie
    #FIXME: добавить vimeo
    text = re.sub('<youtube>http://(?:www\.)?youtube.com/watch\?v=([\w-]+)[^<]*</youtube>', youtubeLink, text)
    text = re.sub('<youtube>http://(?:www\.)?youtube.com/watch\?([\w-]+)=(.+?)</youtube>', youtubeLink, text)
    text = re.sub('<youtube>http://(?:www\.)?youtube.com/v/([\w-]+)</youtube>', youtubeLink, text)
    text = re.sub('<rutube>http://rutube.ru/tracks/\d+.html\?v=([\w-]+)</rutube>', rutubeLink, text)
    text = re.sub('<rutube>(\d+)</rutube>', rutubeId, text)

    for s in settings.SMILES:
        text = re.sub('(' + s + ')', smiles, text)

    BBCODE = {'\[b\]': '<strong>', '\[/b\]': '</strong>', '<blue>': '<span class="text_blue">', '</blue>': '</span>'}
    for b in BBCODE:
        text = re.sub(b, BBCODE[b], text)
    text = re.sub('\[img\](.+?)\[/img\]', r'<img src="\1">', text)

    text = re.sub('\[url\](.+?)\[/url\]', r'<a href="\1" rel="nofollow">\1</a>', text)
    text = re.sub('''(?<!['">=])(http://[a-zA-Z\.%\d\?/_&;=#()-]+)''', r'<a href="\1" rel="nofollow">\1</a>', text)

    return mark_safe(text)

##########################################################


@register.inclusion_tag('block_items_list.html')
def items_list(items):
    return {'items': items}


@register.inclusion_tag('block_items_ul_list.html')
def items_ul_list(items):
    return {'items': items}


@register.inclusion_tag('block_items_table_list.html')
def items_table_list(items):
    return {'items': items}

######################################################


@cached(cache_key='last_conversations', timeout_seconds=settings.CACHE_LONG_TIMEOUT)
def get_last_coversations():
    items = list(Post.objects.filter(status='pub').order_by('-last_comment_date')[:15]) + \
            list(Photo.objects.all().order_by('-last_comment_date')[:15]) + \
            list(Man.objects.all().order_by('-last_comment_date')[:15]) + \
            list(Mountain.objects.all().order_by('-last_comment_date')[:15]) + \
            list(Movie.objects.all().order_by('-last_comment_date')[:15])
    anno = datetime(1900, 1, 1)
    items.sort(key=lambda i: i.last_comment_date or anno, reverse=True)
    items = items[:20]

    authors_ids = [item.author_id for item in items if hasattr(item, 'author_id')]
    authors = User.objects.in_bulk(authors_ids)
    for item in items:
        if hasattr(item, 'author_id'):
            item.author_name = authors[item.author_id].name
        else:
            item.author_name = None

    return items


@register.inclusion_tag('block_last_conversations.html')
def last_conversations():
    return {'last_conversations': get_last_coversations()}


@register.inclusion_tag('block_tags_list.html')
def tags_list(amount=10):
    tags = list(Tag.objects.exclude(name__in=('other', 'video')).order_by('-size')[:amount])
    font_borders = (12, 30)
    size_borders = (tags[-1].size, tags[0].size)
    factor = (font_borders[1] - font_borders[0] + 0.0) / (size_borders[1] - size_borders[0])
    for tag in tags:
        tag.font_size = int((tag.size - size_borders[0]) * factor + font_borders[0])
    tags.sort(key=lambda tag: tag.title)
    return {'tags': tags}


@register.inclusion_tag('block_main_tags_list.html')
def main_tags_list(amount=10):
    tags = Tag.objects.filter(size__gt=1, type__gt=10).order_by('-size')[:amount]
    return {'tags': tags}


@register.filter
def el(dic, key):
    return dic.get(key)


@register.inclusion_tag('block_items_ul_list.html')
def mountains_list(region):
    return {'items': get_mountains(region)['mountains'][:20]}


@register.inclusion_tag('block_soundtrack_list.html')
def soundtrack_list(songs):
    return {'songs': songs}


@register.inclusion_tag('block_soundtrack_list.html')
def soundtrack(movie):
    return {'songs': Song.objects.filter(movie=movie)}


@time_slow(threshold=0)
@register.filter
def link(item):
    if not item:
        return u"[Отсутствует объект]"

    if isinstance(item, Tag):
        return mark_safe(u'<a href="http://%s%s" rel="tag">%s</a>' % (settings.DOMAIN, item.get_absolute_url(), item.title))

    if isinstance(item, User):
        return mark_safe(u'<a href="http://%s%s">%s</a>' % (settings.DOMAIN, item.get_absolute_url(), item.name))

    if isinstance(item, Photo):
        return mark_safe(u'<a href="http://%s%s"><img class="userphoto" src="%s" alt="%s"></a>'
                         % (settings.DOMAIN, item.get_absolute_url(), settings.MEDIA_URL + thumbnail(item.yandex_fotki_image_src), item.title))

    return mark_safe(u'<a href="http://%s%s">%s</a>' % (settings.DOMAIN, item.get_absolute_url(), item.title))


@register.simple_tag
def post_edit_link(post, user):
    if post.can_edit(user):
        return mark_safe('(<a href="%s">ред.</a>)' % reverse('edit_post', args=[post.pk]))
    return ""


@register.simple_tag
def post_status(post):
    if post.status == 'save':
        return u"(черновик)"
    if post.status == 'del':
        return u"(удален)"
    if post.status == 'deferred':
        return u"(будет опубликован %s)" % post.date_created
    return u""


@register.filter
def add_referrer(html, referrer):
    return re.sub(r'href="(http://[^"]+)"', r'href="\1#referrer=%s"' % referrer, html)

################################################################################
# Блоги

# WTF?
@register.simple_tag
def cut_view(post, user, mode='normal'):
    if isinstance(post, Comment):
        template = "block_cut_comment.html"
    else:
        template = "block_cut_post.html"
    try:
        t = loader.get_template(template)
        return t.render(Context({'post': post, 'user': user, 'mode': mode}))
    except TemplateDoesNotExist:
        return link(post)


@register.inclusion_tag('block_post_panel.html')
def post_panel(post, user, mode='normal'):
    return {'post': post,
            'user': user,
            'already_voted': post.get_vote(user) is not None,
            'mode': mode,
            'klass': post.__class__.__name__.lower(),
    }


@cached(cache_key=lambda post, r: '/%s/comments' % post.uid, timeout_seconds=settings.CACHE_LONG_TIMEOUT)
def get_comments(post, request):
    comments = post.comments.filter(status='pub', hidden=False).order_by('order')
    users = User.objects.in_bulk(set(comment.author_id for comment in comments))
    profiles = dict((profile.user_id, profile) for profile in Profile.objects.filter(user__in=users.keys()))
    avatars = Avatar.get(users.keys(), 32)

    for comment in comments:
        comment.author = users[comment.author_id]
        comment.profile = profiles[comment.author_id]
        comment.avatar = avatars[comment.author_id]
        comment.profile_link = link(comment.author)

    context = {'post': post,
               'klass': post.__class__.__name__.lower(),
               'comments': comments,
    }
    result = render_to_string(request, 'blocks/b-comments.html', context)
    return result


@register.simple_tag
def comments(post, request):
    return get_comments(post, request)


@register.filter
def indent(order, add=0):
    return (len(order) + add * 3) * 10


@register.inclusion_tag('block_post_vote.html')
def post_vote_arrows(user, post):
    return {'user': user, 'post': post,
            'can_vote': post.can_vote(user),
            }


@register.simple_tag
def yadirect(block_name):
    template = "yadirect/%s.html" % block_name
    try:
        t = loader.get_template(template)
        return t.render(Context())
    except TemplateDoesNotExist:
        return "Шаблон не найден"


@register.filter
def human_month(monthNumber):
    months = (u'январь', u'февраль', u'март', u'апрель', u'май', u'июнь', u'июль', u'август',
              u'сентябрь', u'октябрь', u'ноябрь', u'декабрь')
    return months[monthNumber - 1]


@register.filter
def thumbnail(image_url):
    return get_thumbnail_url(image_url)

##########################################################################################
# Admin site tags


@register.simple_tag
def get_admin_url(object):
    u"""Ссылка на редактирование эелмента"""
    return u"http://%(domain)s/admind/%(app_label)s/%(module_name)s/%(object_id)s/" % {
        'domain': settings.DOMAIN,
        'app_label': object._meta.app_label,
        'module_name': object._meta.module_name,
        'object_id': quote(unicode(object.pk).encode('utf8'))
    }


@register.inclusion_tag('admin/tag_replace_form.html')
def admin_tag_replace(object_id):
    return {'tag': Tag.objects.get(pk=object_id),
            'object_id': object_id,
            }
