# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AlterModelOptions(
            name='newscategory',
            options={'ordering': ('order',), 'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u043d\u043e\u0432\u043e\u0441\u0442\u0435\u0439', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u043d\u043e\u0432\u043e\u0441\u0442\u0435\u0439'},
        ),
    ]
