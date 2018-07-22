# coding: utf-8

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150830_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_len',
            field=models.PositiveIntegerField(default=0, verbose_name='\u0414\u043b\u0438\u043d\u0430 \u0442\u0435\u043a\u0441\u0442\u0430'),
        ),
    ]
