# coding: utf-8

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151121_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='in_index',
            field=models.NullBooleanField(default=None, verbose_name='\u0412 \u0438\u043d\u0434\u0435\u043a\u0441\u0435'),
        ),
        migrations.AddField(
            model_name='post',
            name='used',
            field=models.BooleanField(default=False, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u043e'),
        ),
    ]
