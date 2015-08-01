# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_id', models.CharField(unique=True, max_length=50, verbose_name='ID')),
                ('status', models.CharField(max_length=50, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441')),
                ('txt', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('url', models.CharField(max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('page', models.CharField(max_length=255, verbose_name='\u0423\u0440\u043b \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b', db_index=True)),
            ],
            options={
                'verbose_name': '\u0421\u0441\u044b\u043b\u043a\u0430',
                'verbose_name_plural': '\u0421\u0441\u044b\u043b\u043a\u0438',
            },
        ),
    ]
