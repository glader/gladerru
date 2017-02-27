# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.core.cache import cache

from redactor.fields import RedactorField
from yafotki.fields import YFField

from core.utils.common import cached, slug, count_text_len


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
    name = models.CharField(max_length=200, verbose_name='Код')
    title = models.CharField(max_length=200, verbose_name='Название')
    checked = models.BooleanField(default=False, verbose_name='Проверен')
    primary_synonim = models.ForeignKey('self', related_name='synonim', verbose_name='Основной синоним',
                                        null=True, blank=True)
    parent = models.ForeignKey('self', related_name='parent_tag', verbose_name='Родитель', null=True, blank=True)
    TYPES = ((10, 'Вид спорта'),
             (20, 'Категория'),
             (30, 'Тег')
             )
    type = models.PositiveIntegerField(choices=TYPES, default=30, verbose_name='Тип')
    size = models.PositiveIntegerField(default=0, verbose_name='Размер')
    posts = models.TextField(verbose_name='Посты', default='')
    need_recalc = models.BooleanField(verbose_name='Требует пересчета', default=False)
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)
    category = models.ForeignKey('NewsCategory', verbose_name='Категория', null=True, blank=True, default=None)

    tags = None

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
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
        return '/tags/%s' % self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = slug(self.title)

        if self.posts:
            self.size = len(self.posts.split(','))

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

        self.posts = ','.join(str(post.id) for post in posts)
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


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='Пользователь')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    date_changed = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', editable=False)

    content = models.TextField(null=True, blank=True, verbose_name='Содержание элемента')
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name='Статус')

    bindings = models.CharField(max_length=250, null=True, blank=True, verbose_name='Крепления')
    birthday = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')
    board = models.CharField(max_length=250, null=True, blank=True, verbose_name='Доска')
    boots = models.CharField(max_length=250, null=True, blank=True, verbose_name='Ботинки')
    clothes = models.CharField(max_length=250, null=True, blank=True, verbose_name='Одежда')
    city = models.CharField(max_length=250, null=True, blank=True, verbose_name='Город')
    country = models.CharField(max_length=250, null=True, blank=True, verbose_name='Страна')
    equip = models.CharField(max_length=250, null=True, blank=True, verbose_name='Снаряга')
    GENDER_CHOICES = (
        ('m', 'Мальчик'),
        ('f', 'Девочка'),
        ('', 'Не определилось'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='', max_length=1, null=True, blank=True,
                              verbose_name='Пол')
    icq = models.CharField(max_length=50, null=True, blank=True, verbose_name='ICQ')
    interests = models.TextField(null=True, blank=True, verbose_name='Интересы')
    is_moderator = models.BooleanField(default=False, verbose_name='Является модератором')
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name='Дата последнего захода на сайт')
    mountains = models.CharField(max_length=250, null=True, blank=True, verbose_name='Горы')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    riding_style = models.CharField(max_length=250, null=True, blank=True, verbose_name='Стиль катания')
    stance = models.CharField(max_length=50, null=True, blank=True, verbose_name='Стойка')
    referer = models.CharField(max_length=250, null=True, blank=True, verbose_name='Откуда пришел')

    pic_count = models.PositiveIntegerField(default=0, verbose_name='Количество картинок')
    pub_post_count = models.PositiveIntegerField(default=0, verbose_name='Количество постов')

    unread_news_count = models.PositiveIntegerField(default=0, verbose_name='Количество непрочитанных анонсов')
    send_news = models.BooleanField(default=True, verbose_name='Отсылать новости сайта')

    def calculate(self):
        self.pub_post_count = Post.objects.filter(author=self.user, status='pub').count()
        self.pic_count = Photo.objects.filter(author=self.user).count()
        self.save()

    def __unicode__(self):
        return self.user.username

    @cached(cache_key=lambda user: '/users/%s/url' % user.id, timeout_seconds=settings.CACHE_LONG_TIMEOUT)
    def get_absolute_url(self):
        return self.user.get_absolute_url()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class UIDMixin(object):
    id = None

    @property
    def uid(self):
        return '%s_%s' % (self.__class__.__name__.lower(), self.id)


class Skill(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.CharField(verbose_name='Код', max_length=200)
    description = models.TextField(verbose_name='Описание')
    image = YFField(verbose_name='Картинка', upload_to='gladerru', null=True, blank=True, default=None)
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('skill', args=[self.slug])

    class Meta:
        verbose_name = 'Умение'
        verbose_name_plural = 'Умения'


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name='Пользователь')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    content = models.TextField(null=True, blank=True, verbose_name='Содержание')
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name='Статус')
    hidden = models.BooleanField(default=False, verbose_name='Скрытый')
    order = models.CharField(max_length=255, null=True, blank=True, verbose_name='Порядок')
    local_url = models.CharField(verbose_name='Адрес', default='', max_length=100)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey()
    ip = models.CharField(verbose_name='IP', null=True, blank=True, max_length=30)

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def get_absolute_url(self):
        return self.local_url

    def __unicode__(self):
        return '%s: %s' % (self.author, self.item)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Comment, self).save(*args, **kwargs)

        cache.delete(settings.CACHE_MIDDLEWARE_KEY_PREFIX + 'last_conversations')
        if self.item:
            cache.delete(settings.CACHE_MIDDLEWARE_KEY_PREFIX + '/%s/comments' % self.item.uid)
            self.local_url = '%s#c%s' % (self.item.get_absolute_url(), self.id)

        return super(Comment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


STATUSES = (
    ('pub', 'Опубликовано'),
    ('save', 'Черновик'),
    ('deferred', 'Отложено'),
    ('del', 'Удалено'),
    ('ban', 'Забанено'),
    ('premoderate', 'Премодерация')
)

TYPES = (
    ('post', 'Пост'),
    ('page', 'Статическая страница'),
)


class Post(models.Model, UIDMixin):
    author = models.ForeignKey(User, null=True, blank=True, verbose_name='Автор')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Урл', max_length=255, null=True, blank=True, default=None)

    category = models.ForeignKey('NewsCategory', verbose_name='Категория', null=True, blank=True, default=None)
    content = RedactorField(null=True, blank=True, verbose_name='Содержание')
    status = models.CharField(choices=STATUSES, default='save', max_length=50, verbose_name='Статус')
    type = models.CharField(choices=TYPES, default='post', max_length=15, verbose_name='Тип поста')

    abstract = models.TextField(null=True, blank=True, verbose_name='Анонс')
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name='Количество комментариев')
    hidden = models.BooleanField(default=False, verbose_name='Скрытый')
    sticky_to = models.DateField(verbose_name='Приклеен до', null=True, blank=True, default=None)
    skill = models.ForeignKey(Skill, null=True, blank=True, verbose_name='Умение')
    icon = YFField(verbose_name='Иконка', null=True, blank=True, upload_to='gladerru', default=None)
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)
    meta_keywords = models.TextField(verbose_name='Keywords', help_text='meta-keywords',
                                     null=True, blank=True, default=None)

    text_len = models.PositiveIntegerField(verbose_name='Длина текста', default=0)
    in_index = models.NullBooleanField(verbose_name='В индексе', blank=True, default=None)
    used = models.BooleanField(verbose_name='Использовано', default=False)
    position = models.FloatField(verbose_name='Позиция', null=True, blank=True, default=None)

    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    comments = GenericRelation(Comment)

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def __unicode__(self):
        return self.title

    @property
    def is_sticky(self):
        return self.sticky_to and self.sticky_to > date.today()

    def get_absolute_url(self):
        if self.skill or self.type == 'page':
            rubric = 'content'
        elif self.category:
            rubric = self.category.slug
        else:
            rubric = 'other'

        return reverse('post', args=[rubric, self.slug])

    def can_edit(self, user):
        return user.is_superuser

    def save(self, *args, **kwargs):
        self.hidden = self.status != 'pub'

        if not self.slug:
            self.slug = slug(self.title)

        self.text_len = count_text_len(self.content or '')

        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Photo(models.Model, UIDMixin):
    slug = models.CharField(max_length=250, null=True, blank=True, verbose_name='Код картинки')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='Заголовок')
    content = models.TextField(null=True, blank=True, verbose_name='Содержание элемента')
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name='Статус')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)

    author = models.ForeignKey(User, verbose_name='Автор', null=True, blank=True, related_name='core_user')
    post = models.ForeignKey(Post, verbose_name='Пост', null=True, blank=True, related_name='core_post')
    rider = models.ForeignKey('movies.Man', verbose_name='Райдер', null=True, blank=True, related_name='core_rider')
    photographer = models.ForeignKey('movies.Man', verbose_name='Фотограф', null=True, blank=True,
                                     related_name='core_photographer')
    place = models.CharField(max_length=250, null=True, blank=True, verbose_name='Место')

    yandex_fotki_image_src = models.CharField(null=True, blank=True, verbose_name='Путь к картинке', max_length=255)

    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    best = models.DateTimeField(null=True, blank=True, verbose_name='На главной')
    local_url = models.CharField(verbose_name='Адрес', max_length=70, default='')

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

    def is_photo(self):
        return True

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        self.local_url = '/users/%s/photos/%s' % (self.author.username.lower(), self.id)
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Word(models.Model, UIDMixin):
    title = models.CharField(verbose_name='Слово', max_length=100)
    slug = models.CharField(verbose_name='Код', max_length=100)
    abstract = models.TextField(verbose_name='Вкратце', null=True, blank=True)
    content = models.TextField(verbose_name='Описание', null=True, blank=True)
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)

    DICTIONARIES = (('common', 'Общий словарь'),
                    ('jib', 'Джиббинг'),
                    ('preparatory', 'Подготовительные'),
                    ('grabs', 'Гребы'),
                    ('spins', 'Вращения'),
                    ('bigspins', 'Продвинутые трюки'),
                    ('jibbing_tricks', 'Джиббинг'),
                    ('pipe_tricks', 'Пайповые прыжки'),
                    ('other_tricks', 'Разное'),
                    )
    type = models.CharField(choices=DICTIONARIES, default='common', verbose_name='Словарь', max_length=20)

    comments = GenericRelation(Comment)

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
        verbose_name = 'Словарное слово'
        verbose_name_plural = 'Словарные слова'

    def has_content(self):
        return bool(self.content) and '+' or ''
    has_content.short_description = 'Есть содержание'


class Keyword(models.Model):
    u""" Автогенерируемая таблица всех характерных слов типа имен райдеров и названий фильмов """
    keyword = models.CharField(verbose_name='Слово', max_length=200)
    url = models.URLField(verbose_name='Ссылка')
    TYPES = (
        ('auto', 'Из другой таблицы'),
        ('manual', 'Руками'),
    )
    type = models.CharField(verbose_name='Тип', max_length=20, choices=TYPES, default='manual')

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name = 'Замена'
        verbose_name_plural = 'Замены'


class Redirect(models.Model):
    u"""Редиректы"""
    source = models.CharField(verbose_name='Откуда', max_length=200)
    destination = models.CharField(verbose_name='Куда', max_length=200)

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
        verbose_name = 'Редирект'
        verbose_name_plural = 'Редиректы'


class NewsCategory(models.Model):
    u"""Категории новостей"""
    title = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(verbose_name='Урл', max_length=255)
    order = models.PositiveIntegerField(verbose_name='Порядок', default=100)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    class Meta:
        ordering = ('order',)
        verbose_name = 'Категория новостей'
        verbose_name_plural = 'Категории новостей'


User.name = property(lambda u: u.first_name or u.username)
User.get_profile = lambda u: Profile.objects.get(user=u)
