# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yafotki.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Man',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(unique=True, max_length=100, verbose_name='\u041a\u043e\u0434')),
                ('content', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('is_rider', models.BooleanField(default=False, verbose_name='\u0420\u0430\u0439\u0434\u0435\u0440')),
                ('is_photographer', models.BooleanField(default=False, verbose_name='\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444')),
                ('is_director', models.BooleanField(default=False, verbose_name='\u0420\u0435\u0436\u0438\u0441\u0441\u0435\u0440')),
                ('angles', models.CharField(max_length=10, null=True, verbose_name='\u0423\u0433\u043b\u044b', blank=True)),
                ('birthday', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('footsize', models.CharField(max_length=10, null=True, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u043d\u043e\u0433\u0438', blank=True)),
                ('gender', models.CharField(default=b'm', max_length=1, verbose_name='\u041f\u043e\u043b', choices=[(b'm', '\u041c\u0430\u043b\u044c\u0447\u0438\u043a'), (b'f', '\u0414\u0435\u0432\u043e\u0447\u043a\u0430')])),
                ('image', yafotki.fields.YFField(default=None, upload_to=b'gladerru', max_length=255, blank=True, null=True, verbose_name='\u041f\u043e\u0440\u0442\u0440\u0435\u0442')),
                ('ridingsince', models.PositiveIntegerField(null=True, verbose_name='\u041a\u0430\u0442\u0430\u0435\u0442\u0441\u044f \u0441 \u0433\u043e\u0434\u0430', blank=True)),
                ('stance', models.CharField(max_length=50, null=True, verbose_name='\u0421\u0442\u043e\u0439\u043a\u0430', blank=True)),
                ('width', models.CharField(max_length=50, null=True, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430', blank=True)),
                ('url', models.URLField(max_length=250, null=True, verbose_name='URL', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='\u0421\u043a\u0440\u044b\u0442')),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
                ('primary_synonim', models.ForeignKey(related_name='synonim', verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0441\u0438\u043d\u043e\u043d\u0438\u043c', blank=True, to='movies.Man', null=True)),
            ],
            options={
                'verbose_name': '\u0427\u0435\u043b\u043e\u0432\u0435\u043a',
                'verbose_name_plural': '\u041b\u044e\u0434\u0438',
            },
        ),
        migrations.CreateModel(
            name='Man2Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'actor', max_length=20, verbose_name='\u0420\u043e\u043b\u044c', choices=[(b'actor', '\u0420\u0430\u0439\u0434\u0435\u0440'), (b'director', '\u0420\u0435\u0436\u0438\u0441\u0441\u0435\u0440')])),
                ('man', models.ForeignKey(verbose_name='\u0427\u0435\u043b\u043e\u0432\u0435\u043a', to='movies.Man')),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0439\u0434\u0435\u0440 \u0444\u0438\u043b\u044c\u043c\u0430',
                'verbose_name_plural': '\u0420\u0430\u0439\u0434\u0435\u0440\u044b \u0444\u0438\u043b\u044c\u043c\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(unique=True, max_length=100, verbose_name='\u041a\u043e\u0434')),
                ('content', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('url', models.URLField(max_length=250, null=True, verbose_name='URL', blank=True)),
                ('cover', yafotki.fields.YFField(default=None, upload_to=b'gladerru', max_length=255, blank=True, null=True, verbose_name='\u041e\u0431\u043b\u043e\u0436\u043a\u0430')),
                ('torrent', models.URLField(max_length=250, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0442\u043e\u0440\u0440\u0435\u043d\u0442', blank=True)),
                ('teaser', models.TextField(null=True, verbose_name='\u0422\u0438\u0437\u0435\u0440', blank=True)),
                ('full_movie', models.TextField(null=True, verbose_name='\u0412\u0438\u0434\u0435\u043e', blank=True)),
                ('has_songs', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u0442\u0440\u0435\u043a\u043b\u0438\u0441\u0442')),
                ('year', models.PositiveIntegerField(null=True, verbose_name='\u0413\u043e\u0434 \u0432\u044b\u043f\u0443\u0441\u043a\u0430', blank=True)),
                ('rating', models.FloatField(default=0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
                ('dt_teaser_added', models.DateTimeField(default=None, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u0442\u0438\u0437\u0435\u0440\u0430', blank=True)),
                ('dt_fullmovie_added', models.DateTimeField(default=None, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u043d\u043e\u0444\u043e\u0440\u043c\u0430\u0442\u043d\u043e\u0433\u043e \u0440\u043e\u043b\u0438\u043a\u0430', blank=True)),
                ('dt_soundtrack_added', models.DateTimeField(default=None, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u0441\u0430\u0443\u043d\u0434\u0442\u0440\u0435\u043a\u0430', blank=True)),
            ],
            options={
                'verbose_name': '\u0424\u0438\u043b\u044c\u043c',
                'verbose_name_plural': '\u0424\u0438\u043b\u044c\u043c\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('yandex_fotki_image_src', models.CharField(max_length=255, null=True, verbose_name='\u041f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435', blank=True)),
                ('rating', models.IntegerField(default=0, help_text='\u0411\u044b\u043b \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d \u043f\u043e \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u0430\u043c \u043f\u0440\u0438 \u0441\u043b\u0443\u0447\u0430\u0439\u043d\u043e\u043c \u043f\u043e\u043a\u0430\u0437\u0435', verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('photographer', models.ForeignKey(related_name='photographer', verbose_name='\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444', blank=True, to='movies.Man', null=True)),
                ('rider', models.ForeignKey(related_name='rider', verbose_name='\u0420\u0430\u0439\u0434\u0435\u0440', blank=True, to='movies.Man', null=True)),
            ],
            options={
                'verbose_name': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('performer', models.CharField(max_length=200, null=True, verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', blank=True)),
                ('title', models.CharField(max_length=200, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='\u0414\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c', blank=True)),
                ('file', models.FileField(upload_to=b'data/mp3', null=True, verbose_name='\u0424\u0430\u0439\u043b', blank=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a', blank=True)),
                ('note', models.CharField(max_length=200, null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435', blank=True)),
                ('filename', models.CharField(max_length=200, null=True, verbose_name='\u0418\u043c\u044f \u0444\u0430\u0439\u043b\u0430', blank=True)),
                ('movie', models.ForeignKey(verbose_name='\u0424\u0438\u043b\u044c\u043c', to='movies.Movie')),
            ],
            options={
                'ordering': ('movie', 'order'),
                'verbose_name': '\u041f\u0435\u0441\u043d\u044f',
                'verbose_name_plural': '\u041f\u0435\u0441\u043d\u0438',
            },
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(unique=True, max_length=100, verbose_name='\u041a\u043e\u0434')),
                ('content', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('url', models.URLField(max_length=250, null=True, verbose_name='URL', blank=True)),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0443\u0434\u0438\u044f',
                'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0438\u0438',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='studio',
            field=models.ForeignKey(verbose_name='\u0421\u0442\u0443\u0434\u0438\u044f', blank=True, to='movies.Studio', null=True),
        ),
        migrations.AddField(
            model_name='man2movie',
            name='movie',
            field=models.ForeignKey(verbose_name='\u0424\u0438\u043b\u044c\u043c', to='movies.Movie'),
        ),
    ]
