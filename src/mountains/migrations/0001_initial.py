# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import votes.models
import yafotki.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u041e\u0431\u043b\u0430\u0441\u0442\u044c',
                'verbose_name_plural': '\u041e\u0431\u043b\u0430\u0441\u0442\u0438',
            },
        ),
        migrations.CreateModel(
            name='Mountain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=250, unique=True, null=True, verbose_name='\u041a\u043e\u0434 \u0433\u043e\u0440\u044b', blank=True)),
                ('title', models.CharField(max_length=250, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430', blank=True)),
                ('status', models.CharField(max_length=50, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', blank=True)),
                ('address', models.CharField(max_length=200, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441', blank=True)),
                ('has_ratrack', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u0440\u0430\u0442\u0440\u0430\u043a')),
                ('hidden', models.BooleanField(default=False, verbose_name='\u0421\u043a\u0440\u044b\u0442\u044b\u0439')),
                ('image', yafotki.fields.YFField(default=None, upload_to=b'gladerru', max_length=255, blank=True, null=True, verbose_name='\u0421\u0445\u0435\u043c\u0430 \u0442\u0440\u0430\u0441\u0441')),
                ('lifts', models.TextField(null=True, verbose_name='\u041f\u043e\u0434\u044a\u0435\u043c\u043d\u0438\u043a\u0438', blank=True)),
                ('latitude', models.CharField(max_length=20, null=True, verbose_name='\u0428\u0438\u0440\u043e\u0442\u0430', blank=True)),
                ('longitude', models.CharField(max_length=20, null=True, verbose_name='\u0414\u043e\u043b\u0433\u043e\u0442\u0430', blank=True)),
                ('longest', models.CharField(max_length=50, null=True, verbose_name='\u0421\u0430\u043c\u0430\u044f \u0434\u043b\u0438\u043d\u043d\u0430\u044f \u0442\u0440\u0430\u0441\u0441\u0430', blank=True)),
                ('nightwork', models.TextField(help_text='\u0414\u043e \u0441\u043a\u043e\u043b\u044c\u043a\u0438', null=True, verbose_name='\u041d\u043e\u0447\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430', blank=True)),
                ('oldschool', models.BooleanField(default=False, verbose_name='\u041e\u043b\u0434\u0441\u043a\u0443\u043b')),
                ('overfall', models.CharField(max_length=50, null=True, verbose_name='\u041f\u0435\u0440\u0435\u043f\u0430\u0434 \u0432\u044b\u0441\u043e\u0442', blank=True)),
                ('pistelength', models.CharField(max_length=50, null=True, verbose_name='\u041e\u0431\u0449\u0430\u044f \u0434\u043b\u0438\u043d\u0430 \u0442\u0440\u0430\u0441\u0441', blank=True)),
                ('pistes', models.CharField(max_length=50, null=True, verbose_name='\u041a\u043e\u043b-\u0432\u043e \u0442\u0440\u0430\u0441\u0441', blank=True)),
                ('prices', models.TextField(null=True, verbose_name='\u0426\u0435\u043d\u044b', blank=True)),
                ('rating', models.FloatField(default=0.0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('service', models.TextField(null=True, verbose_name='\u0423\u0441\u043b\u0443\u0433\u0438', blank=True)),
                ('snowpark', models.TextField(null=True, verbose_name='\u0421\u043d\u043e\u0443\u043f\u0430\u0440\u043a', blank=True)),
                ('tel', models.CharField(max_length=250, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d\u044b', blank=True)),
                ('url', models.URLField(max_length=250, null=True, verbose_name='URL', blank=True)),
                ('webcam', models.URLField(max_length=250, null=True, verbose_name='Web \u043a\u0430\u043c\u0435\u0440\u0430', blank=True)),
                ('work_time', models.TextField(max_length=50, null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0431\u043e\u0442\u044b', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True)),
                ('interactive_map', models.TextField(default=None, null=True, verbose_name='\u0418\u043d\u0442\u0435\u0440\u0430\u043a\u0442. \u043a\u0430\u0440\u0442\u0430', blank=True)),
                ('newbie', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u0443\u0447\u0435\u0431\u043d\u044b\u0439 \u0441\u043a\u043b\u043e\u043d')),
                ('parking', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u043f\u043b\u0430\u0442\u043d\u0430\u044f \u0441\u0442\u043e\u044f\u043d\u043a\u0430')),
                ('rental', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u043f\u0440\u043e\u043a\u0430\u0442 \u043e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u044f')),
                ('room', models.BooleanField(default=False, verbose_name='\u041a\u043e\u043c\u043d\u0430\u0442\u0430 \u0434\u043b\u044f \u043f\u0435\u0440\u0435\u043e\u0434\u0435\u0432\u0430\u043d\u0438\u044f')),
                ('safe', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u043a\u0430\u043c\u0435\u0440\u0430 \u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f')),
                ('has_service', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u043c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u0430\u044f/\u0441\u0435\u0440\u0432\u0438\u0441')),
                ('cafe', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u043a\u0430\u0444\u0435')),
                ('hotel', models.TextField(null=True, verbose_name='\u0413\u043e\u0441\u0442\u0438\u043d\u0438\u0446\u0430', blank=True)),
                ('has_light', models.BooleanField(default=False, verbose_name='\u0415\u0441\u0442\u044c \u043e\u0441\u0432\u0435\u0449\u0435\u043d\u0438\u0435 \u0442\u0440\u0430\u0441\u0441')),
                ('has_show', models.BooleanField(default=False, verbose_name='\u0418\u0441\u043a\u0443\u0441\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439 \u0441\u043d\u0435\u0433')),
                ('check_date', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438', blank=True)),
                ('proof_url', models.TextField(null=True, verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0434\u0430\u043d\u043d\u044b\u0445', blank=True)),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
                ('district', models.ForeignKey(verbose_name='\u041e\u0431\u043b\u0430\u0441\u0442\u044c', blank=True, to='mountains.District', null=True)),
            ],
            options={
                'verbose_name': '\u0413\u043e\u0440\u0430',
                'verbose_name_plural': '\u0413\u043e\u0440\u044b',
            },
            bases=(models.Model, votes.models.VoteMixin),
        ),
        migrations.CreateModel(
            name='MountainPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', yafotki.fields.YFField(upload_to=b'gladerru', max_length=255, verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430')),
                ('mountain', models.ForeignKey(verbose_name=b'\xd0\x93\xd0\xbe\xd1\x80\xd0\xb0', to='mountains.Mountain')),
            ],
            options={
                'verbose_name': '\u0424\u043e\u0442\u043e \u0433\u043e\u0440\u044b',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e \u0433\u043e\u0440',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('order', models.PositiveIntegerField(verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a')),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u0420\u0435\u0433\u0438\u043e\u043d',
                'verbose_name_plural': '\u0420\u0435\u0433\u0438\u043e\u043d\u044b',
            },
        ),
        migrations.AddField(
            model_name='mountain',
            name='region',
            field=models.ForeignKey(verbose_name='\u0420\u0435\u0433\u0438\u043e\u043d', to='mountains.Region'),
        ),
    ]
