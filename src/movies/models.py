# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from yafotki.fields import YFField
from votes.models import VoteMixin

from core.utils.thumbnails import make_thumbnail
from .utils import ID3


class GenericManager(models.Manager):
    """
    Filters query set with given selectors
    """
    def __init__(self, **kwargs):
        super(GenericManager, self).__init__()
        self.selectors = kwargs

    def get_query_set(self):
        return super(GenericManager, self).get_query_set().filter(**self.selectors)


class Man(models.Model):
    title = models.CharField(verbose_name=u"Название", max_length=100, unique=True)
    slug = models.CharField(verbose_name=u"Код", max_length=100, unique=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    is_rider = models.BooleanField(verbose_name=u"Райдер", default=False)
    is_photographer = models.BooleanField(verbose_name=u"Фотограф", default=False)
    is_director = models.BooleanField(verbose_name=u"Режиссер", default=False)
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
    hidden = models.BooleanField(verbose_name=u"Скрыт", default=False)
    comment_count = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Количество комментариев")
    last_comment_date = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата последнего комментария",
                                             editable=False)
    primary_synonim = models.ForeignKey('self', related_name='synonim', verbose_name=u"Основной синоним",
                                        null=True, blank=True)
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)

    objects = GenericManager()
    interesting = GenericManager(hidden=False)

    def get_absolute_url(self):
        if self.primary_synonim:
            return reverse('man', args=[self.primary_synonim.slug])
        elif self.slug:
            return reverse('man', args=[self.slug])
        else:
            return reverse('man', args=[self.id])

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.hidden = True
        for f in ['content', 'angles', 'birthday', 'footsize', 'ridingsince', 'sponsors', 'stance',
                  'url', 'width', 'image']:
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
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)

    def get_absolute_url(self):
        return reverse('studio', args=[self.slug])

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Студия"
        verbose_name_plural = u"Студии"


class Movie(models.Model, VoteMixin):
    title = models.CharField(verbose_name=u"Название", max_length=100, unique=True)
    slug = models.CharField(verbose_name=u"Код", max_length=100, unique=True)
    studio = models.ForeignKey(Studio, verbose_name=u"Студия", null=True, blank=True)
    content = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"URL")
    cover = YFField(verbose_name=u"Обложка", upload_to='gladerru', null=True, blank=True, default=None)
    torrent = models.URLField(max_length=250, null=True, blank=True, verbose_name=u"Ссылка на торрент")
    teaser = models.TextField(verbose_name=u"Тизер", null=True, blank=True)
    full_movie = models.TextField(verbose_name=u"Видео", null=True, blank=True)
    has_songs = models.BooleanField(verbose_name=u"Есть треклист", default=False)
    year = models.PositiveIntegerField(verbose_name=u"Год выпуска", null=True, blank=True)
    rating = models.FloatField(verbose_name=u"Рейтинг", default=0)
    date_created = None
    meta_description = models.TextField(verbose_name=u"Description", help_text=u"meta-description",
                                        null=True, blank=True, default=None)
    dt_teaser_added = models.DateTimeField(verbose_name=u'Дата добавления тизера', null=True,
                                           blank=True, default=None)
    dt_fullmovie_added = models.DateTimeField(verbose_name=u'Дата добавления полноформатного ролика', null=True,
                                              blank=True, default=None)
    dt_soundtrack_added = models.DateTimeField(verbose_name=u'Дата добавления саундтрека', null=True,
                                               blank=True, default=None)

    def get_absolute_url(self):
        return reverse('movie', kwargs={'year': self.year or '-', 'slug': self.slug})

    def __unicode__(self):
        return self.title

    @property
    def uid(self):
        return "%s_%s" % (self.__class__.__name__.lower(), self.id)

    def save(self, *args, **kwargs):
        if self.pk:
            movie = Movie.objects.get(pk=self.pk)
            if self.teaser and not movie.teaser:
                self.dt_teaser_added = datetime.now()
            if self.full_movie and not movie.full_movie:
                self.dt_fullmovie_added = datetime.now()
        if self.cover:
            make_thumbnail(str(self.cover.src()))
        return super(Movie, self).save(*args, **kwargs)

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
                id3info = ID3.ID3(path)
                self.performer = id3info['ARTIST'].decode('cp1251')
                self.title = id3info['TITLE'].decode('cp1251')
                if not self.movie.has_songs:
                    self.movie.has_songs = True
                    self.movie.dt_soundtrack_added = datetime.now()
                    self.movie.save()
            except ID3.InvalidTagError, message:
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


class Photo(models.Model, VoteMixin):
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=u"Заголовок")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)
    rider = models.ForeignKey(Man, verbose_name=u"Райдер", null=True, blank=True, related_name="rider")
    photographer = models.ForeignKey(Man, verbose_name=u"Фотограф", null=True, blank=True, related_name="photographer")
    yandex_fotki_image_src = models.CharField(null=True, blank=True, verbose_name=u"Путь к картинке", max_length=255)

    rating = models.IntegerField(verbose_name=u"Рейтинг", default=0,
                                 help_text=u"Был составлен по переходам при случайном показе")

    def __unicode__(self):
        return self.title or unicode(self.id)

    @property
    def uid(self):
        return "%s_%s" % (self.__class__.__name__.lower(), self.id)

    def is_photo(self):
        return True

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Фотография"
        verbose_name_plural = u"Фотографии"
