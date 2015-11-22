# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151122_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='position',
            field=models.FloatField(default=None, verbose_name='\u041f\u043e\u0437\u0438\u0446\u0438\u044f', blank=True),
        ),
    ]
