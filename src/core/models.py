# -*- coding: utf-8 -*-
import Image
import os
import uuid
from utils.ID3 import *
import random
from StringIO import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.template import Context, loader
from django_queue.models import Queue
from django.core.cache import cache
from django.core.mail import send_mail

from yafotki.fields import YFField

from core.utils.common import cached, slug
from core.utils.log import get_logger
from core.utils.thumbnails import make_thumbnail


class GenericManager(models.Manager):
    """
    Filters query set with given selectors
    """
    def __init__(self, **kwargs):
        super(GenericManager, self).__init__()
        self.selectors = kwargs

    def get_query_set(self):
        return super(GenericManager, self).get_query_set().filter(**self.selectors)


class Tag(models.Model):
    u"""Теги"""
    name = models.CharField(max_length=200, verbose_name=u"Код")
    title = models.CharField(max_length=200, verbose_name=u"Название")
    checked = models.BooleanField(default=False, verbose_name=u"Проверен")
    primary_synonim = models.ForeignKey('self', related_name='synonim', verbose_name=u"Основной синоним", null=True, blank=True)
    parent = models.ForeignKey('self', related_name='parent_tag', verbose_name=u"Родитель", null=True, blank=True)
    TYPES = ((10, u'Вид спорта'),
             (20, u'Категория'),
             (30, u'Тег')
             )
    type = models.PositiveIntegerField(choices=TYPES, default=30, verbose_name=u"Тип")
    size = models.PositiveIntegerField(default=0, verbose_name=u"Размер")
    posts = models.TextField(verbose_name=u"Посты", default="")
    need_recalc = models.BooleanField(verbose_name=u"Требует пересчета", default=False)

    tags = None

    class Meta:
        verbose_name = u"Тег"
        verbose_name_plural = u"Теги"
        ordering = ['-type', '-size']

    @staticmethod
    def process_tags(tags_str):
        """ Создает теги по строке """
        if not tags_str:
            return []
        tags = [t.strip() for t in tags_str.split(',')]
        tag_slugs = [slug(t.strip()) for t in tags_str.split(',')]

        present_tags = dict((t.title.lower(), t) for t in Tag.objects.filter(title__in=tags))
        present_tags.update(dict((t.name.lower(), t) for t in Tag.objects.filter(name__in=tags)))
        present_tags.update(dict((t.name.lower(), t) for t in Tag.objects.filter(name__in=tag_slugs)))

        result = []
        for tag_title in tags:
            lower_title = tag_title.lower()
            if lower_title in present_tags:
                tag = present_tags[lower_title]
            elif slug(tag_title) in present_tags:
                tag = present_tags[slug(tag_title)]
            else:
                tag = Tag.objects.create(name=slug(tag_title), title=tag_title, size=1)

            if tag.primary_synonim:
                result.append(tag.primary_synonim)
            else:
                result.append(tag)

        return result

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/tags/%s" % self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = slug(self.title)

        if self.posts:
            self.size = len(self.posts.split(','))

        if self.new_synonim():
            from core.tasks import tag_synonim
            tag_synonim.delay(self.id)

        super(Tag, self).save(*args, **kwargs)

    def new_synonim(self):
        u"""Новый синоним у тега"""
        if not self.primary_synonim:
            return False

        old_tag = Tag.objects.get(pk=self.id)
        if self.primary_synonim == old_tag.primary_synonim:
            return False

        return True

    @classmethod
    def get_tag(cls, title):
        u"""Поиск по имени тега регистрозависимо. MySQL похоже так не умеет"""
        tags = cls.objects.filter(title=title)
        for t in tags:
            if t.title == title:
                return t
        return None

    def recalc_posts(self):
        u"""Пересчитать список постов, относящихся к этому тегу"""
        tags = self.get_children()
        posts = Post.objects.filter(tags__in=tags, hidden=False).order_by('-date_created')

        self.posts = ",".join(str(post.id) for post in posts)
        self.save()

    def get_children(self):
        u"""Список всех потомков"""
        children = []
        current = [self]
        while len(current):
            tag = current.pop()
            children.append(tag)
            for t in Tag.objects.filter(parent=tag):
                if t not in children:
                    current.append(t)

        return children

    def remove_post_from_cache(self, post):
        id = str(post.id)
        self.posts = self.posts.replace(id + ',', '').replace(id, '')
        self.save()

    @classmethod
    def get_by_query(cls, query, limit=10):
        if not cls.tags:
            cls.fetch_tags()

        tags = [t for t in cls.tags if query.lower() in t.title.lower() or query.lower() in t.name.lower()]
        tags.sort(key=lambda t: (-t.size, t.title))
        tags = tags[:limit]
        tags.sort(key=lambda t: t.title)
        return tags

    @classmethod
    def fetch_tags(cls):
        cls.tags = list(cls.objects.filter(primary_synonim__isnull=True))


class TagsCloud(object):
    def __init__(self, tags):
        self.tags = tags

    def set_rel_sizes(self, min_rel_size=1, max_rel_size=1):
        min = None
        max = 1
        for tag in self.tags:
            tag.size = int(tag.size)
            if min is None or min > tag.size:
                min = tag.size
            if max < tag.size:
                max = tag.size

        for tag in self.tags:
            if min == max:
                tag.rel_size = (max_rel_size + min_rel_size) / 2

            else:
                tag.rel_size = min_rel_size + \
                            (tag.size - min) * (max_rel_size - min_rel_size) / (max - min)


def get_image_path(instance, filename):
    paths = {'MOVIE': 'images/covers/%s',
             'RIDER': 'portraits/%s',
             'PHOTOGRAPHER': 'portraits/%s',
             'MEN_OTHER': 'portraits/%s',
             'FIRM': 'images/logo/%s',
             'SHOP': 'images/logo/%s',
             'MAGAZINE': 'images/logo/%s',
             'MOVIE_MAKER': 'images/logo/%s',
             'TEAM': 'images/logo/%s',
             }

    if isinstance(instance, Photo):
        user = instance.author
        user_dir = os.path.join(settings.STATIC_ROOT, 'data', 'users', user.username)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)

        return 'data/users/%s/%s.jpg' % (user.username, uuid.uuid4().hex)

    elif instance.type.name in paths:
        return paths[instance.type.name] % filename

    return 'data/other/%s' % filename


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u"Пользователь")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    date_changed = models.DateTimeField(auto_now=True, verbose_name=u"Дата изменения", editable=False)

    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Статус")

    avatar = models.BooleanField(default=False, blank=True, verbose_name=u"Аватар")
    bindings = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Крепления")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата рождения")
    board = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Доска")
    boots = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Ботинки")
    clothes = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Одежда")
    city = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Город")
    country = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Страна")
    equip = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Снаряга")
    GENDER_CHOICES = (
        ('m', u'Мальчик'),
        ('f', u'Девочка'),
        ('', u'Не определилось'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='', max_length=1, null=True, blank=True, verbose_name=u"Пол")
    icq = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"ICQ")
    interests = models.TextField(null=True, blank=True, verbose_name=u"Интересы")
    is_moderator = models.BooleanField(default=False, verbose_name=u"Является модератором")
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего захода на сайт")
    mountains = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Горы")
    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    riding_style = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Стиль катания")
    stance = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Стойка")
    referer = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Откуда пришел")

    comment_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество комментариев")
    pic_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество картинок")
    pub_post_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество постов")
    unread_comment_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество непрочитанных комментариев")

    unread_news_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество непрочитанных анонсов")
    send_news = models.BooleanField(default=True, verbose_name=u"Отсылать новости сайта")

    def calculate(self):
        self.comment_count = Comment.objects.filter(author=self.user).count()
        self.pub_post_count = Post.objects.filter(author=self.user, status='pub').count()
        self.pic_count = Photo.objects.filter(author=self.user).count()
        self.save()

    def __unicode__(self):
        return self.user.username

    @cached(cache_key=lambda user: "/users/%s/url" % user.id, timeout_seconds=settings.CACHE_LONG_TIMEOUT)
    def get_absolute_url(self):
        return self.user.get_absolute_url()

    class Meta:
        verbose_name = u"Профиль"
        verbose_name_plural = u"Профили"


class Avatar(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Юзер", db_index=True, unique=True)
    avatar128 = YFField(upload_to='gladerru')
    avatar64 = YFField(upload_to='gladerru')
    avatar32 = YFField(upload_to='gladerru')
    avatar16 = YFField(upload_to='gladerru')

    def __unicode__(self):
        return self.user.username

    @classmethod
    def add(cls, user, file):
        try:
            avatar = cls.objects.get(user=user)
        except cls.DoesNotExist:
            avatar = cls(user=user)

        import imghdr
        file.seek(0)
        format = imghdr.what('', file.read(2048)) or 'jpeg'
        file.seek(0)

        for size in (128, 64, 32, 16):
            file.seek(0)
            im = Image.open(file)
            im.thumbnail((size, size), Image.ANTIALIAS)
            th = StringIO()

            im.save(th, format)
            th.seek(0)
            image = th.read()

            class F(StringIO):
                pass

            uploaded_file = F(image)
            uploaded_file.name = 'avatar_%s' % size
            uploaded_file.size = 1
            uploaded_file.file = image

            getattr(avatar, 'avatar%s' % size).save('avatar_%s' % size, uploaded_file)

        avatar.save()

        user.get_profile().avatar = True
        user.get_profile().save()

    @classmethod
    def get(cls, users, size):
        users = [user.id if isinstance(user, User) else user for user in users]
        avatars = dict((a.user_id, a) for a in Avatar.objects.filter(user__in=users))
        return dict((user_id, getattr(avatars[user_id], 'avatar%s' % size).src
                                if user_id in avatars
                                else "%sdesign/3/img/avatars/avatar%s.png" % (settings.STATIC_URL, size)
            )
            for user_id in users
        )

    class Meta:
        verbose_name = u"Аватар"
        verbose_name_plural = u"Аватары"


class Friend(models.Model):
    user_a = models.ForeignKey(User, verbose_name=u"Кто дружит", related_name='object')
    user_b = models.ForeignKey(User, verbose_name=u"С кем дружит", related_name='subject')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)

    def __unicode__(self):
        return u"%s дружит с %s" % (self.user_a.username, self.user_b.username)

    class Meta:
        verbose_name = u"Дружба"
        verbose_name_plural = u"Друзья"
        unique_together = (("user_a", "user_b"),)


class News(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    TYPE_CHOICES = (
        ('new_post', u'Ваш друг добавил пост'),
        ('new_friend', u'Ваш друг добавил друга'),
        ('new_comment', u'Ваш друг добавил комментарий'),
        ('new_trip', u'Друг добавил новую поездку'),
        ('good_post', u'Новый пост на главной'),
        ('tagged_post', u'Новый пост в теге'),
        ('new_movie', u'Описание нового фильма'),
        ('new_teaser', u'Выложен новый тизер'),
        ('new_tracklist', u'Выложен треклист фильма'),
        ('new_fullmovie', u'Выложен полноформатный фильм'),
    )
    type = models.CharField(choices=TYPE_CHOICES, default='', max_length=20, verbose_name=u"Тип")
    content = models.TextField(verbose_name=u"Содержание")

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey()

    messages = {'new_post': u'<a href="http://glader.ru%(user_url)s">%(username)s</a> написал новый пост: <a href="http://glader.ru%(post_url)s">%(post_title)s</a>',
                'tagged_post': u'В теге <a href="http://glader.ru%(tag_url)s">%(tag_title)s</a> появился новый пост: <a href="http://glader.ru%(post_url)s">%(post_title)s</a>',
                'good_post': u'Новый пост в лучших: <a href="http://glader.ru%(post_url)s">%(post_title)s</a>',
                'new_friend': u'<a href="http://glader.ru%(user_url)s">%(username)s</a> добавил в друзья <a href="http://glader.ru%(friend_url)s">%(friend_title)s</a>',
                'new_teaser': u'Выложен тизер фильма <a href="http://glader.ru%(movie_url)s">%(movie_title)s</a>',
                'new_fullmovie': u'Выложено полноформатное видео <a href="http://glader.ru%(movie_url)s">%(movie_title)s</a>',
                'new_tracklist': u'Выложен саундтрек к фильму <a href="http://glader.ru%(movie_url)s">%(movie_title)s</a>',
                }

    def __unicode__(self):
        return u"%s - %s" % (self.type, self.content)

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"


class UserNews(models.Model):
    u""" Новости юзеров """
    user = models.ForeignKey(User, verbose_name=u"Юзер")
    news = models.ForeignKey(News, verbose_name=u"Новость", null=True, default=None)

    def __unicode__(self):
        return u"%s - %s" % (self.user.username, self.news)

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"

    def save(self, *args, **kwargs):
        if not self.pk:
            profile = self.user.get_profile()
            profile.unread_news_count += 1
            profile.save()

        return super(UserNews, self).save(*args, **kwargs)


class ItemVote(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Пользователь")
    vote = models.IntegerField(verbose_name=u"Оценка")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    ip = models.CharField(verbose_name=u"IP", null=True, blank=True, max_length=30)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey()

    class Meta:
        verbose_name = u"Оценка"
        verbose_name_plural = u"Оценки"


class VoteMixin(object):
    pk = None
    author = None

    def get_vote(self, user):
        """ Возвращает оценку, выставленную элементу юзером. None, если не голосовал """
        #FIXME: добавить votes = generic.GenericRelation(ItemVote)
        if user and user.is_authenticated():
            votes = ItemVote.objects.filter(content_type__pk=26, object_id=self.pk, user=user)
            if votes:
                return reduce(lambda x, y: x + y, [v.vote for v in votes])
        return None

    def can_vote(self, user):
        if not user:
            return False
        if not user.is_authenticated():
            return False
        if user.get_profile().is_moderator:
            return True
        if hasattr(self, 'author') and self.author == user:
            return False
        return self.get_vote(user) is None


class UIDMixin(object):
    id = None

    @property
    def uid(self):
        return "%s_%s" % (self.__class__.__name__.lower(), self.id)


class Skill(models.Model):
    title = models.CharField(verbose_name=u"Название", max_length=200)
    slug = models.CharField(verbose_name=u"Код", max_length=200)
    description = models.TextField(verbose_name=u"Описание")
    image = YFField(verbose_name=u"Картинка", upload_to='gladerru', null=True, blank=True, default=None)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('skill', args=[self.slug])

    class Meta:
        verbose_name = u"Умение"
        verbose_name_plural = u"Умения"


class Tag2Skill(models.Model):
    skill = models.ForeignKey(Skill, verbose_name=u"Умение")
    tag = models.ForeignKey(Tag, verbose_name=u"Тег")

    class Meta:
        verbose_name = u"Тег умения"
        verbose_name_plural = u"Теги умений"


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Пользователь")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Статус")
    hidden = models.BooleanField(default=False, verbose_name=u"Скрытый")
    order = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Порядок")
    local_url = models.CharField(verbose_name=u"Адрес", default="", max_length=100)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey()
    ip = models.CharField(verbose_name=u"IP", null=True, blank=True, max_length=30)

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def get_absolute_url(self):
        return self.local_url

    def __unicode__(self):
        return u"%s: %s" % (self.author, self.item)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Comment, self).save(*args, **kwargs)

        cache.delete(settings.CACHE_MIDDLEWARE_KEY_PREFIX + 'last_conversations')
        if self.item:
            cache.delete(settings.CACHE_MIDDLEWARE_KEY_PREFIX + '/%s/comments' % self.item.uid)
            self.local_url = "%s#c%s" % (self.item.get_absolute_url(), self.id)

        return super(Comment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Комментарий"
        verbose_name_plural = u"Комментарии"


class Rubric(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name=u"Имя элемента")
    parent = models.ForeignKey('self', verbose_name=u"Родитель", null=True, blank=True)
    template = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Шаблон")
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    abstract = models.TextField(null=True, blank=True, verbose_name=u"Анонс")
    image = YFField(upload_to='gladerru', null=True, blank=True, verbose_name=u"Картинка")
    menu_type = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Тип меню")
    order = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Порядок")
    skill = models.ForeignKey(Skill, null=True, blank=True, verbose_name=u"Умение")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rubric', args=[self.name])

    class Meta:
        verbose_name = u"Рубрика"
        verbose_name_plural = u"Рубрики"


STATUSES = (
    ('pub', u'Опубликовано'),
    ('save', u'Черновик'),
    ('deferred', u'Отложено'),
    ('del', u'Удалено'),
    ('ban', u'Забанено'),
    ('premoderate', u'Премодерация')
)

TYPES = (
    ('post', u'Пост'),
    ('teaser', u'Тизер фильма'),
    ('full_movie', u'Полноформатный фильм'),
    ('soundtrack', u'Музыка к фильму'),
)


class Post(models.Model, VoteMixin, UIDMixin):
    name = models.CharField(max_length=250, null=True, blank=True, default=None, unique=True, verbose_name=u"Имя элемента")
    author = models.ForeignKey(User, null=True, blank=True, verbose_name=u"Автор")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    type = models.CharField(choices=TYPES, default='post', max_length=15, verbose_name=u"Тип поста")

    abstract = models.TextField(null=True, blank=True, verbose_name=u"Анонс")
    best = models.DateTimeField(null=True, blank=True, verbose_name=u"На главной")
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    event_date_start = models.DateTimeField(null=True, blank=True, default=None, verbose_name=u"Дата начала события")
    event_date_finish = models.DateTimeField(null=True, blank=True, default=None, verbose_name=u"Дата окончания события")
    hidden = models.BooleanField(default=False, verbose_name=u"Скрытый")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария", editable=False)
    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    rubric = models.ForeignKey(Rubric, null=True, blank=True, verbose_name=u"Рубрика")
    skill = models.ForeignKey(Skill, null=True, blank=True, verbose_name=u"Умение")
    tags_str = models.TextField(null=True, blank=True, verbose_name=u"Теги")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    is_question = models.BooleanField(verbose_name=u"Вопрос", default=False)
    best_answer = models.ForeignKey(Comment, verbose_name=u"Лучший ответ", null=True, blank=True, related_name="post_best_answer")
    ask_for_answer_amount = models.PositiveSmallIntegerField(verbose_name=u"Количество напоминаний", default=0,
                                                             help_text=u"Сколько раз напомнили о необходимости выбира лучшего ответа")
    ip = models.CharField(verbose_name=u"IP", null=True, blank=True, max_length=30)
    icon = YFField(verbose_name=u"Иконка", null=True, blank=True, upload_to='gladerru', default=None)
    local_url = models.CharField(verbose_name=u"Адрес", max_length=70, default="")

    tags = models.ManyToManyField(Tag, verbose_name=u"Теги", null=True, blank=True)
    comments = generic.GenericRelation(Comment)

    # привязка анонсов к фильмам
    item_type = models.ForeignKey(ContentType, null=True, blank=True)
    item_id = models.PositiveIntegerField(null=True, blank=True)
    item = generic.GenericForeignKey('item_type', 'item_id')

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.local_url

    def can_edit(self, user):
        if not user:
            return False
        if not user.is_authenticated():
            return False
        if user.get_profile().is_moderator:
            return True
        return self.author == user

    def tags_html(self):
        if self.tags_str is None:
            self.rebuild_tags()
        return self.tags_str

    def rebuild_tags(self):
        tags = self.tags.all().order_by('type', '-size')
        t = loader.get_template('block_post_tags.html')
        self.tags_str = unicode(t.render(Context({'tags': tags})))
        self.save()

    def save(self, *args, **kwargs):
        self.is_question = False
        if self.pk:
            for t in self.tags.all():
                if t.name == 'question':
                    self.is_question = True

            self.drop_cache()

        if self.status != 'pub':
            self.hidden = True
        else:
            self.hidden = False

        if self.name and not self.name.startswith('post'):
            local_url = "/content/%s.htm" % self.name
        else:
            local_url = "/users/%s/posts/%s" % (self.author.username.lower(), self.id)
        self.local_url = local_url

        super(Post, self).save(*args, **kwargs)

    def drop_cache(self):
        cache.delete("%srender/post/%s/%s" % (settings.CACHE_ROOT, self.id, 'cut'))
        cache.delete("%srender/post/%s/%s" % (settings.CACHE_ROOT, self.id, 'full'))

    class Meta:
        verbose_name = u"Пост"
        verbose_name_plural = u"Посты"


class Region(models.Model):
    """ Регион """
    title = models.CharField(max_length=250, verbose_name=u"Название")
    order = models.PositiveIntegerField(verbose_name=u"Порядок")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("region", args=[self.id])

    class Meta:
        verbose_name = u"Регион"
        verbose_name_plural = u"Регионы"
        ordering = ['order']


class District(models.Model):
    """ Область """
    title = models.CharField(max_length=250, verbose_name=u"Название")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("district", args=[self.id])

    class Meta:
        verbose_name = u"Область"
        verbose_name_plural = u"Области"


class Mountain(models.Model, VoteMixin, UIDMixin):
    name = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name=u"Имя элемента")
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Статус")

    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Адрес")
    district = models.ForeignKey(District, null=True, blank=True, verbose_name=u"Область")
    has_ratrack = models.BooleanField(default=False, verbose_name=u"Есть ратрак")
    hidden = models.BooleanField(default=False, verbose_name=u"Скрытый")
    image = YFField(upload_to="gladerru", null=True, blank=True, verbose_name=u"Схема трасс", default=None)
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария", editable=False)
    lifts = models.TextField(null=True, blank=True, verbose_name=u"Подъемники")
    latitude = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"Широта")
    longitude = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"Долгота")
    longest = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Самая длинная трасса")
    nightwork = models.TextField(null=True, blank=True, verbose_name=u"Ночная работа", help_text=u"До скольки")
    oldschool = models.BooleanField(default=False, verbose_name=u"Олдскул")
    overfall = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Перепад высот")
    pistelength = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Общая длина трасс")
    pistes = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Кол-во трасс")
    prices = models.TextField(null=True, blank=True, verbose_name=u"Цены")
    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    region = models.ForeignKey(Region, verbose_name=u"Регион")
    root_tag = models.ForeignKey(Tag, null=True, blank=True, verbose_name=u"Тег")
    service = models.TextField(null=True, blank=True, verbose_name=u"Услуги")
    snowpark = models.TextField(null=True, blank=True, verbose_name=u"Сноупарк")
    tel = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Телефоны")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    webcam = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"Web камера")
    work_time = models.TextField(max_length=50, null=True, blank=True, verbose_name=u"Время работы")
    email = models.EmailField(null=True, blank=True, verbose_name=u"Email")

    newbie = models.BooleanField(default=False, verbose_name=u"Есть учебный склон")
    parking = models.BooleanField(default=False, verbose_name=u"Есть платная стоянка")
    rental = models.BooleanField(default=False, verbose_name=u"Есть прокат оборудования")
    room = models.BooleanField(default=False, verbose_name=u"Комната для переодевания")
    safe = models.BooleanField(default=False, verbose_name=u"Есть камера хранения")
    has_service = models.BooleanField(default=False, verbose_name=u"Есть мастерская/сервис")
    cafe = models.BooleanField(default=False, verbose_name=u"Есть кафе")
    hotel = models.TextField(null=True, blank=True, verbose_name=u"Гостиница")
    has_light = models.BooleanField(default=False, verbose_name=u"Есть освещение трасс")
    has_show = models.BooleanField(default=False, verbose_name=u"Искусственный снег")

    check_date = models.DateField(null=True, blank=True, verbose_name=u"Дата обработки")
    proof_url = models.TextField(null=True, blank=True, verbose_name=u"Источник данных")

    comments = generic.GenericRelation(Comment)
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария", editable=False)

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def get_absolute_url(self):
        return reverse("mountain", args=[self.name])

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Гора"
        verbose_name_plural = u"Горы"


class MountainPhoto(models.Model):
    mountain = models.ForeignKey(Mountain, verbose_name="Гора")
    image = YFField(upload_to='gladerru', verbose_name=u"Картинка")

    class Meta:
        verbose_name = u"Фото горы"
        verbose_name_plural = u"Фото гор"


class Man(models.Model):
    title = models.CharField(verbose_name=u"Название", max_length=100, unique=True)
    slug = models.CharField(verbose_name=u"Код", max_length=100, unique=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    is_rider = models.BooleanField(verbose_name=u"Райдер", default=False)
    is_photographer = models.BooleanField(verbose_name=u"Фотограф", default=False)
    is_director = models.BooleanField(verbose_name=u"Режиссер", default=False)
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    angles = models.CharField(max_length=10, null=True, blank=True, verbose_name=u"Углы")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата рождения")
    footsize = models.CharField(max_length=10, null=True, blank=True, verbose_name=u"Размер ноги")
    GENDER_CHOICES = (
        ('m', u'Мальчик'),
        ('f', u'Девочка'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='m', max_length=1, verbose_name=u"Пол")
    image = YFField(verbose_name=u"Портрет", upload_to='gladerru', null=True, blank=True, default=None)
    ridingsince = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Катается с года")
    sponsors = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Спонсоры")
    stance = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Стойка")
    width = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Ширина")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    tag = models.ForeignKey(Tag, verbose_name=u"Основной тег", null=True, blank=True)
    hidden = models.BooleanField(verbose_name=u"Скрыт", default=False)
    comments = generic.GenericRelation(Comment)
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария", editable=False)
    primary_synonim = models.ForeignKey('self', related_name='synonim', verbose_name=u"Основной синоним", null=True, blank=True)

    objects = GenericManager()
    interesting = GenericManager(hidden=False)

    def get_absolute_url(self):
        if self.primary_synonim:
            return reverse('man', args=[self.primary_synonim.slug])
        else:
            return reverse('man', args=[self.slug])

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.hidden = True
        for f in ['content', 'angles', 'birthday', 'footsize', 'ridingsince', 'sponsors', 'stance', 'url', 'width', 'image']:
            if getattr(self, f):
                self.hidden = False
                break

        if Man2Movie.objects.filter(man=self).count() > 1:
            self.hidden = False

        super(Man, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Человек"
        verbose_name_plural = u"Люди"


class Studio(models.Model):
    title = models.CharField(verbose_name=u"Название", max_length=100, unique=True)
    slug = models.CharField(verbose_name=u"Код", max_length=100, unique=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")

    all = GenericManager()
    objects = GenericManager(status='pub')

    def get_absolute_url(self):
        return reverse('studio', args=[self.slug])

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Студия"
        verbose_name_plural = u"Студии"


class Movie(models.Model, VoteMixin, UIDMixin):
    title = models.CharField(verbose_name=u"Название", max_length=100, unique=True)
    slug = models.CharField(verbose_name=u"Код", max_length=100, unique=True)
    studio = models.ForeignKey(Studio, verbose_name=u"Студия", null=True, blank=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    cover = YFField(verbose_name=u"Обложка", upload_to='gladerru', null=True, blank=True, default=None)
    torrent = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"Ссылка на торрент")
    teaser = models.TextField(verbose_name=u"Тизер", null=True, blank=True)
    full_movie = models.TextField(verbose_name=u"Видео", null=True, blank=True)
    has_songs = models.BooleanField(verbose_name=u"Есть треклист", default=False)
    year = models.PositiveIntegerField(verbose_name=u"Год выпуска", null=True, blank=True)
    rating = models.FloatField(verbose_name=u"Рейтинг", default=0)
    tag = models.ForeignKey(Tag, verbose_name=u"Основной тег", null=True, blank=True)
    hidden = models.BooleanField(verbose_name=u"Скрыт", default=False)
    comments = generic.GenericRelation(Comment)
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария", editable=False)
    date_created = None

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def get_absolute_url(self):
        return reverse('movie', args=[self.slug])

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        report = ""
        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            header = u"Измененные поля фильма %s (%s)" % (self.title, self.get_absolute_url())
            for field in self._meta.fields:
                if field.name in ('comment_count', 'last_comment_date'):
                    continue

                if getattr(self, field.name) != getattr(prev, field.name):
                    report += u"%s: '%s' -> '%s'\n" % (field.verbose_name, getattr(prev, field.name) or '-', getattr(self, field.name) or '-')
        else:
            header = u"Новый фильм %s (%s)" % (self.title, self.get_absolute_url())
            for field in self._meta.fields:
                if field.name in ('comment_count', 'last_comment_date'):
                    continue
                report += u"%s: '%s'\n" % (field.verbose_name, getattr(self, field.name) or '-')

        if report:
            send_mail(
                u"Glader.ru: %s" % header,
                report,
                None,
                ['glader.ru@gmail.com']
            )

        super(Movie, self).save(*args, **kwargs)

        if self.cover:
            make_thumbnail(str(self.cover.src()))

    class Meta:
        verbose_name = u"Фильм"
        verbose_name_plural = u"Фильмы"


class Man2Movie(models.Model):
    man = models.ForeignKey(Man, verbose_name=u"Человек")
    movie = models.ForeignKey(Movie, verbose_name=u"Фильм")
    ROLES = (('actor', u'Райдер'),
             ('director', u'Режиссер'),
             )
    role = models.CharField(choices=ROLES, default='actor', verbose_name=u"Роль", max_length=20)

    def __unicode__(self):
        return u"%s - %s (%s)" % (self.movie, self.man, self.role)

    class Meta:
        verbose_name = u"Райдер фильма"
        verbose_name_plural = u"Райдеры фильмов"


class Photo(models.Model, VoteMixin, UIDMixin):
    slug = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Код картинки")
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)

    author = models.ForeignKey(User, verbose_name=u"Автор", null=True, blank=True)
    post = models.ForeignKey(Post, verbose_name=u"Пост", null=True, blank=True)
    rider = models.ForeignKey(Man, verbose_name=u"Райдер", null=True, blank=True, related_name="rider")
    photographer = models.ForeignKey(Man, verbose_name=u"Фотограф", null=True, blank=True, related_name="photographer")
    place = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Место")

    yandex_fotki_image_src = models.CharField(null=True, blank=True, verbose_name=u"Путь к картинке", max_length=255)

    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    best = models.DateTimeField(null=True, blank=True, verbose_name=u"На главной")
    local_url = models.CharField(verbose_name=u"Адрес", max_length=70, default="")

    tags_str = models.TextField(null=True, blank=True, verbose_name=u"Теги")
    tags = models.ManyToManyField(Tag, verbose_name=u"Теги", null=True, blank=True)

    comments = generic.GenericRelation(Comment)
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария", editable=False)

    all = GenericManager()
    objects = GenericManager(status='pub')

    def __unicode__(self):
        return self.title or unicode(self.id)

    @property
    def hidden(self):
        return self.status != 'pub'

    def get_absolute_url(self):
        return self.local_url

    def can_edit(self, user):
        if not user:
            return False
        if not user.is_authenticated():
            return False
        if user.get_profile().is_moderator:
            return True
        return self.author == user

    def tags_html(self):
        if self.tags_str is None:
            self.rebuild_tags()
        return self.tags_str

    def rebuild_tags(self):
        tags = self.tags.all().order_by('type', '-size')
        t = loader.get_template('block_post_tags.html')
        self.tags_str = unicode(t.render(Context({'tags': tags})))
        self.save()

    def is_photo(self):
        return True

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        self.local_url = "/users/%s/photos/%s" % (self.author.username.lower(), self.id)
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Фотография"
        verbose_name_plural = u"Фотографии"


class PictureBox(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Посетитель", null=True, blank=True)
    picture = models.ForeignKey(Photo, verbose_name=u"Картинка")
    TYPE_CHOICES = (
        ('good', u'Переход'),
        ('next', u'Следующая'),
        ('bad', u'Фигня'),
    )
    action = models.CharField(choices=TYPE_CHOICES, default='', max_length=20, verbose_name=u"Тип")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата-время")

    log = get_logger('picturebox')

    @classmethod
    def get_next_picture(cls, user=None):
        pic_count = Photo.objects.filter(best__isnull=False).count()
        number = random.randrange(pic_count)
        picture = Photo.objects.filter(best__isnull=False)[number]

        cls.log.info('%s: show (%s)', picture.pk, user and user.username or '')
        return picture

    def save(self, *args, **kwargs):
        self.log.info('%s: %s (%s)', self.picture.pk, self.action, self.user and self.user.username or '')
        return super(PictureBox, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Оценка фотографии"
        verbose_name_plural = u"Оценки фотографий"


class Song(models.Model):
    movie = models.ForeignKey(Movie, verbose_name=u"Фильм")
    performer = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Исполнитель")
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Название")
    duration = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Длительность")
    file = models.FileField(verbose_name=u"Файл", null=True, blank=True, upload_to='data/mp3')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Порядок")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Примечание")
    filename = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Имя файла")

    def __unicode__(self):
        return "%s - %s" % (self.performer, self.title)

    def save(self, *args, **kwargs):
        super(Song, self).save(*args, **kwargs)

        if self.file and not (self.performer or self.title):
            try:
                path = os.path.join(settings.STATIC_ROOT, self.file.name)
                os.chmod(path, 0644)
                id3info = ID3(path)
                self.performer = id3info['ARTIST'].decode('cp1251')
                self.title = id3info['TITLE'].decode('cp1251')
                if not self.movie.has_songs:
                    self.movie.has_songs = True
                    self.movie.save()
            except InvalidTagError, message:
                print "Invalid ID3 tag:", message

        if not self.order:
            songs = self.movie.song_set.all().order_by('-order')
            if songs:
                self.order = songs[0].order + 1
            else:
                self.order = 1

        super(Song, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Песня"
        verbose_name_plural = u"Песни"
        ordering = ('movie', 'order')


class Word(models.Model, UIDMixin):
    title = models.CharField(verbose_name=u"Слово", max_length=100)
    slug = models.CharField(verbose_name=u"Код", max_length=100)
    abstract = models.TextField(verbose_name=u"Вкратце", null=True, blank=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)

    DICTIONARIES = (('common', u'Общий словарь'),
                    ('jib', u'Джиббинг'),
                    ('preparatory', u'Подготовительные'),
                    ('grabs', u'Гребы'),
                    ('spins', u'Вращения'),
                    ('bigspins', u'Продвинутые трюки'),
                    ('jibbing_tricks', u'Джиббинг'),
                    ('pipe_tricks', u'Пайповые прыжки'),
                    ('other_tricks', u'Разное'),
                    )
    type = models.CharField(choices=DICTIONARIES, default='common', verbose_name=u"Словарь", max_length=20)

    comments = generic.GenericRelation(Comment)

    def get_absolute_url(self):
        if self.is_trick:
            return reverse('trick', args=[self.slug])
        else:
            return reverse('dictionary_word', args=[self.slug])

    @property
    def is_trick(self):
        return self.type not in ('common', 'jib')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Словарное слово"
        verbose_name_plural = u"Словарные слова"

    def has_content(self):
        return bool(self.content) and u"+" or ""
    has_content.short_description = u"Есть содержание"


class Keyword(models.Model):
    u""" Автогенерируемая таблица всех характерных слов типа имен райдеров и названий фильмов """
    keyword = models.CharField(verbose_name=u"Слово", max_length=200)
    url = models.URLField(verbose_name=u"Ссылка")
    TYPES = (('auto', u'Из другой таблицы'),
            ('manual', u'Руками'),
            )
    type = models.CharField(verbose_name=u"Тип", max_length=20, choices=TYPES, default='manual')

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name = u"Замена"
        verbose_name_plural = u"Замены"


class Discount(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Пользователь")
    city = models.CharField(verbose_name=u"Город", max_length=200)
    card = models.CharField(verbose_name=u"Карточка", max_length=200)
    discount = models.CharField(verbose_name=u"Скидка", max_length=20)
    contacts = models.TextField(verbose_name=u"Контакты", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)

    def __unicode__(self):
        return "%s %s" % (self.card, self.discount)

    class Meta:
        verbose_name = u"Дисконтная карта"
        verbose_name_plural = u"Дисконтные карты"


class Redirect(models.Model):
    u"""Редиректы"""
    source = models.CharField(verbose_name=u"Откуда", max_length=200)
    destination = models.CharField(verbose_name=u"Откуда", max_length=200)

    def __unicode__(self):
        return self.source

    redirects = None

    @classmethod
    def prefetch(cls):
        cls.redirects = dict((r.source, r.destination) for r in cls._default_manager.all())

    @classmethod
    def find(cls, source):
        if not cls.redirects:
            cls.prefetch()

        return cls.redirects.get(source)

    class Meta:
        verbose_name = u"Редирект"
        verbose_name_plural = u"Редиректы"


class UserVisitStat(models.Model):
    u"""Дни заходов юзеров на сайт"""
    user = models.ForeignKey(User, verbose_name=u"Пользователь")
    day = models.DateField(verbose_name=u"Дата")

    def __unicode__(self):
        return "%s - %s" % (self.user, self.day)

    class Meta:
        verbose_name = u"Дата визита"
        verbose_name_plural = u"Даты визитов"


#User.profile = property(lambda u: Item.objects.get_or_create(user=u)[0])
User.name = property(lambda u: u.first_name or u.username)
