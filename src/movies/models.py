# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models

from yafotki.fields import YFField

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
    title = models.CharField(verbose_name='Название', max_length=100, unique=True)
    slug = models.CharField(verbose_name='Код', max_length=100, unique=True)
    content = models.TextField(verbose_name='Описание', null=True, blank=True)
    is_rider = models.BooleanField(verbose_name='Райдер', default=False)
    is_photographer = models.BooleanField(verbose_name='Фотограф', default=False)
    is_director = models.BooleanField(verbose_name='Режиссер', default=False)
    angles = models.CharField(max_length=10, null=True, blank=True, verbose_name='Углы')
    birthday = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')
    footsize = models.CharField(max_length=10, null=True, blank=True, verbose_name='Размер ноги')
    GENDER_CHOICES = (
        ('m', 'Мальчик'),
        ('f', 'Девочка'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='m', max_length=1, verbose_name='Пол')
    image = YFField(verbose_name='Портрет', upload_to='gladerru', null=True, blank=True, default=None)
    ridingsince = models.PositiveIntegerField(null=True, blank=True, verbose_name='Катается с года')
    stance = models.CharField(max_length=50, null=True, blank=True, verbose_name='Стойка')
    width = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ширина')
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name='URL')
    hidden = models.BooleanField(verbose_name='Скрыт', default=False)
    primary_synonim = models.ForeignKey('self', related_name='synonim', verbose_name='Основной синоним',
                                        null=True, blank=True)
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
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
        self.hidden = Man2Movie.objects.filter(man=self).count() <= 1

        for f in ['content', 'angles', 'birthday', 'footsize', 'ridingsince', 'stance',
                  'url', 'width', 'image']:
            if getattr(self, f):
                self.hidden = False
                break

        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            if self.primary_synonim and not prev.primary_synonim:
                self.rider.update(rider=self.primary_synonim)
                self.photographer.update(photographer=self.primary_synonim)
                Man2Movie.objects.filter(man=self).update(man=self.primary_synonim)

                content_fields = (
                    'content', 'angles', 'birthday', 'footsize', 'gender', 'image', 'ridingsince',
                    'stance', 'width', 'url',
                )
                for field in content_fields:
                    if getattr(self, field, None) and not getattr(self.primary_synonim, field, None):
                        setattr(self.primary_synonim, field, getattr(self, field, None))

                self.primary_synonim.hidden = False
                self.primary_synonim.save()

        super(Man, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'


class Studio(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100, unique=True)
    slug = models.CharField(verbose_name='Код', max_length=100, unique=True)
    content = models.TextField(verbose_name='Описание', null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name='URL')
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)

    def get_absolute_url(self):
        return reverse('studio', args=[self.slug])

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'


class Movie(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100, unique=True)
    slug = models.CharField(verbose_name='Код', max_length=100, unique=True)
    studio = models.ForeignKey(Studio, verbose_name='Студия', null=True, blank=True)
    content = models.TextField(verbose_name='Описание', null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True, verbose_name='URL')
    cover = YFField(verbose_name='Обложка', upload_to='gladerru', null=True, blank=True, default=None)
    torrent = models.URLField(max_length=250, null=True, blank=True, verbose_name='Ссылка на торрент')
    teaser = models.TextField(verbose_name='Тизер', null=True, blank=True)
    full_movie = models.TextField(verbose_name='Видео', null=True, blank=True)
    has_songs = models.BooleanField(verbose_name='Есть треклист', default=False)
    year = models.PositiveIntegerField(verbose_name='Год выпуска', null=True, blank=True)
    rating = models.FloatField(verbose_name='Рейтинг', default=0)
    meta_description = models.TextField(verbose_name='Description', help_text='meta-description',
                                        null=True, blank=True, default=None)
    dt_teaser_added = models.DateTimeField(verbose_name='Дата добавления тизера', null=True,
                                           blank=True, default=None)
    dt_fullmovie_added = models.DateTimeField(verbose_name='Дата добавления полноформатного ролика', null=True,
                                              blank=True, default=None)
    dt_soundtrack_added = models.DateTimeField(verbose_name='Дата добавления саундтрека', null=True,
                                               blank=True, default=None)

    def get_absolute_url(self):
        return reverse('movie', kwargs={'year': self.year or '-', 'slug': self.slug})

    def __unicode__(self):
        return self.title

    @property
    def uid(self):
        return '%s_%s' % (self.__class__.__name__.lower(), self.id)

    def save(self, *args, **kwargs):
        report = ''
        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            header = 'Измененные поля фильма %s (%s)' % (self.title, self.get_absolute_url())
            for field in self._meta.fields:
                if field.name in ('comment_count', 'last_comment_date'):
                    continue

                if getattr(self, field.name) != getattr(prev, field.name):
                    report += '%s: "%s" -> "%s"\n' % \
                              (field.verbose_name, getattr(prev, field.name) or '-', getattr(self, field.name) or '-')
        else:
            header = 'Новый фильм %s (%s)' % (self.title, self.get_absolute_url())
            for field in self._meta.fields:
                if field.name in ('comment_count', 'last_comment_date'):
                    continue
                report += '%s: "%s"\n' % (field.verbose_name, getattr(self, field.name) or '-')

        if report:
            send_mail(
                'Glader.ru: %s' % header,
                report,
                None,
                ['glader.ru@gmail.com']
            )

        if self.pk:
            movie = Movie.objects.get(pk=self.pk)
            if self.teaser and not movie.teaser:
                self.dt_teaser_added = datetime.now()
            if self.full_movie and not movie.full_movie:
                self.dt_fullmovie_added = datetime.now()
        else:
            if self.teaser:
                self.dt_teaser_added = datetime.now()
            if self.full_movie:
                self.dt_fullmovie_added = datetime.now()

        obj = super(Movie, self).save(*args, **kwargs)

        if self.cover:
            make_thumbnail(str(self.cover.src()))
        return obj

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Man2Movie(models.Model):
    man = models.ForeignKey(Man, verbose_name='Человек')
    movie = models.ForeignKey(Movie, verbose_name='Фильм')
    ROLES = (('actor', 'Райдер'),
             ('director', 'Режиссер'),
             )
    role = models.CharField(choices=ROLES, default='actor', verbose_name='Роль', max_length=20)

    def __unicode__(self):
        return '%s - %s (%s)' % (self.movie, self.man, self.role)

    class Meta:
        verbose_name = 'Райдер фильма'
        verbose_name_plural = 'Райдеры фильмов'


class Song(models.Model):
    movie = models.ForeignKey(Movie, verbose_name='Фильм')
    performer = models.CharField(max_length=200, null=True, blank=True, verbose_name='Исполнитель')
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название')
    duration = models.PositiveIntegerField(default=0, blank=True, verbose_name='Длительность')
    file = models.FileField(verbose_name='Файл', null=True, blank=True, upload_to='data/mp3')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name='Порядок')
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name='Примечание')
    filename = models.CharField(max_length=200, null=True, blank=True, verbose_name='Имя файла')

    def __unicode__(self):
        return '%s - %s' % (self.performer, self.title)

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
                print 'Invalid ID3 tag:', message

        if not self.order:
            songs = self.movie.song_set.all().order_by('-order')
            if songs:
                self.order = songs[0].order + 1
            else:
                self.order = 1

        super(Song, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'
        ordering = ('movie', 'order')


class Photo(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='Заголовок')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', editable=False)
    rider = models.ForeignKey(Man, verbose_name='Райдер', null=True, blank=True, related_name='rider')
    photographer = models.ForeignKey(Man, verbose_name='Фотограф', null=True, blank=True, related_name='photographer')
    yandex_fotki_image_src = models.CharField(null=True, blank=True, verbose_name='Путь к картинке', max_length=255)

    rating = models.IntegerField(verbose_name='Рейтинг', default=0,
                                 help_text='Был составлен по переходам при случайном показе')

    def __unicode__(self):
        return self.title or unicode(self.id)

    @property
    def uid(self):
        return '%s_%s' % (self.__class__.__name__.lower(), self.id)

    def is_photo(self):
        return True

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
