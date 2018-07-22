# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yafotki.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mountain',
            name='image',
            field=yafotki.fields.YFField(default=None, upload_to='gladerr', max_length=255, blank=True, null=True, verbose_name='\u0421\u0445\u0435\u043c\u0430 \u0442\u0440\u0430\u0441\u0441'),
        ),
        migrations.AlterField(
            model_name='mountain',
            name='work_time',
            field=models.TextField(null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0431\u043e\u0442\u044b', blank=True),
        ),
        migrations.AlterField(
            model_name='mountainphoto',
            name='image',
            field=yafotki.fields.YFField(upload_to='gladerr', max_length=255, verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430'),
        ),
        migrations.AlterField(
            model_name='mountainphoto',
            name='mountain',
            field=models.ForeignKey(on_delete=models.DO_NOTHING, verbose_name='\u0413\u043e\u0440\u0430', to='mountains.Mountain'),
        ),
    ]
