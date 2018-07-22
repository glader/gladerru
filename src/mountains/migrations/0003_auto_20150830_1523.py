# coding: utf-8

from django.db import models, migrations
import yafotki.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0002_auto_20150807_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mountain',
            name='image',
            field=yafotki.fields.YFField(default=None, upload_to='gladerru', max_length=255, blank=True, null=True, verbose_name='\u0421\u0445\u0435\u043c\u0430 \u0442\u0440\u0430\u0441\u0441'),
        ),
        migrations.AlterField(
            model_name='mountainphoto',
            name='image',
            field=yafotki.fields.YFField(upload_to='gladerru', max_length=255, verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430'),
        ),
    ]
