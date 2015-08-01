# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=200, verbose_name='\u0413\u043e\u0440\u043e\u0434')),
                ('card', models.CharField(max_length=200, verbose_name='\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0430')),
                ('discount', models.CharField(max_length=20, verbose_name='\u0421\u043a\u0438\u0434\u043a\u0430')),
                ('contacts', models.TextField(null=True, verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0414\u0438\u0441\u043a\u043e\u043d\u0442\u043d\u0430\u044f \u043a\u0430\u0440\u0442\u0430',
                'verbose_name_plural': '\u0414\u0438\u0441\u043a\u043e\u043d\u0442\u043d\u044b\u0435 \u043a\u0430\u0440\u0442\u044b',
            },
        ),
    ]
