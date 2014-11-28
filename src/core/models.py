# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.core.cache import cache

from redactor.fields import RedactorField
from yafotki.fields import YFField
from votes.models import VoteMixin

from core.utils.common import cached, slug


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
    primary_synonim = models.ForeignKey('self', related_name='synonim', verbose_name=u"Основной синоним",
                                        null=True, blank=True)
    parent = models.ForeignKey('self', related_name='parent_tag', verbose_name=u"Родитель", null=True, blank=True)
    TYPES = ((10, u'Вид спорта'),
             (20, u'Категория'),
             (30, u'Тег')
             )
    type = models.PositiveIntegerField(choices=TYPES, default=30, verbose_name=u"Тип")
    size = models.PositiveIntegerField(default=0, verbose_name=u"Размер")
    posts = models.TextField(verbose_name=u"Посты", default="")
    need_recalc = models.BooleanField(verbose_name=u"Требует пересчета", default=False)
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)
    category = models.ForeignKey('NewsCategory', verbose_name=u"Категория", null=True, blank=True, default=None)

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


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u"Пользователь")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    date_changed = models.DateTimeField(auto_now=True, verbose_name=u"Дата изменения", editable=False)

    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Статус")

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
    gender = models.CharField(choices=GENDER_CHOICES, default='', max_length=1, null=True, blank=True,
                              verbose_name=u"Пол")
    icq = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"ICQ")
    interests = models.TextField(null=True, blank=True, verbose_name=u"Интересы")
    is_moderator = models.BooleanField(default=False, verbose_name=u"Является модератором")
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего захода на сайт")
    mountains = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Горы")
    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    riding_style = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Стиль катания")
    stance = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"Стойка")
    referer = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Откуда пришел")

    pic_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество картинок")
    pub_post_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество постов")

    unread_news_count = models.PositiveIntegerField(default=0, verbose_name=u"Количество непрочитанных анонсов")
    send_news = models.BooleanField(default=True, verbose_name=u"Отсылать новости сайта")

    def calculate(self):
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
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('skill', args=[self.slug])

    class Meta:
        verbose_name = u"Умение"
        verbose_name_plural = u"Умения"


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
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)

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
    ('page', u'Статическая страница'),
)


class Post(models.Model, VoteMixin, UIDMixin):
    name = models.CharField(max_length=250, null=True, blank=True, default=None, verbose_name=u"Имя элемента")
    author = models.ForeignKey(User, null=True, blank=True, verbose_name=u"Автор")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    slug = models.SlugField(verbose_name=u"Урл", max_length=255, null=True, blank=True, default=None)

    category = models.ForeignKey('NewsCategory', verbose_name=u"Категория", null=True, blank=True, default=None)
    content = RedactorField(null=True, blank=True, verbose_name=u"Содержание")
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    type = models.CharField(choices=TYPES, default='post', max_length=15, verbose_name=u"Тип поста")

    abstract = models.TextField(null=True, blank=True, verbose_name=u"Анонс")
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    hidden = models.BooleanField(default=False, verbose_name=u"Скрытый")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария",
                                             editable=False)
    rubric = models.ForeignKey(Rubric, null=True, blank=True, verbose_name=u"Рубрика")
    skill = models.ForeignKey(Skill, null=True, blank=True, verbose_name=u"Умение")
    icon = YFField(verbose_name=u"Иконка", null=True, blank=True, upload_to='gladerru', default=None)
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)

    tags = models.ManyToManyField(Tag, verbose_name=u"Теги", null=True, blank=True)
    comments = generic.GenericRelation(Comment)

    all = GenericManager()
    objects = GenericManager(hidden=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.name:
            return reverse('article', args=[self.name])
        else:
            return reverse('post', args=[self.category.slug, self.id])

    def can_edit(self, user):
        return user.is_superuser

    def save(self, *args, **kwargs):
        self.hidden = self.status != 'pub'
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Пост"
        verbose_name_plural = u"Посты"


class Photo(models.Model, VoteMixin, UIDMixin):
    slug = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Код картинки")
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    content = models.TextField(null=True, blank=True, verbose_name=u"Содержание элемента")
    status = models.CharField(choices=STATUSES, default='pub', max_length=50, verbose_name=u"Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)

    author = models.ForeignKey(User, verbose_name=u"Автор", null=True, blank=True, related_name="core_user")
    post = models.ForeignKey(Post, verbose_name=u"Пост", null=True, blank=True, related_name="core_post")
    rider = models.ForeignKey('movies.Man', verbose_name=u"Райдер", null=True, blank=True, related_name="core_rider")
    photographer = models.ForeignKey('movies.Man', verbose_name=u"Фотограф", null=True, blank=True,
                                     related_name="core_photographer")
    place = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Место")

    yandex_fotki_image_src = models.CharField(null=True, blank=True, verbose_name=u"Путь к картинке", max_length=255)

    rating = models.FloatField(default=0.0, verbose_name=u"Рейтинг")
    best = models.DateTimeField(null=True, blank=True, verbose_name=u"На главной")
    local_url = models.CharField(verbose_name=u"Адрес", max_length=70, default="")

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

        self.local_url = "/users/%s/photos/%s" % (self.author.username.lower(), self.id)
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Фотография"
        verbose_name_plural = u"Фотографии"


class Word(models.Model, UIDMixin):
    title = models.CharField(verbose_name=u"Слово", max_length=100)
    slug = models.CharField(verbose_name=u"Код", max_length=100)
    abstract = models.TextField(verbose_name=u"Вкратце", null=True, blank=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)

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
    TYPES = (
        ('auto', u'Из другой таблицы'),
        ('manual', u'Руками'),
    )
    type = models.CharField(verbose_name=u"Тип", max_length=20, choices=TYPES, default='manual')

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name = u"Замена"
        verbose_name_plural = u"Замены"


class Redirect(models.Model):
    u"""Редиректы"""
    source = models.CharField(verbose_name=u"Откуда", max_length=200)
    destination = models.CharField(verbose_name=u"Куда", max_length=200)

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


class NewsCategory(models.Model):
    u"""Категории новостей"""
    title = models.CharField(verbose_name=u"Название", max_length=255)
    slug = models.SlugField(verbose_name=u"Урл", max_length=255)
    order = models.PositiveIntegerField(verbose_name=u"Порядок", default=100)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    class Meta:
        verbose_name = u"Категория новостей"
        verbose_name_plural = u"Категории новостей"


class Image(models.Model):
    u"""Картинки"""
    upload = YFField(upload_to="gladerru")


User.name = property(lambda u: u.first_name or u.username)
