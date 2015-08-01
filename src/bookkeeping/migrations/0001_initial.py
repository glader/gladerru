# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=50, verbose_name='\u0410\u043a\u043a\u0430\u0443\u043d\u0442', choices=[(b'glader', 'Glader'), (b'skyslayer', 'Skyslayer')])),
                ('amount', models.DecimalField(verbose_name='\u0421\u0443\u043c\u043c\u0430', max_digits=12, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u043e')),
                ('comment', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': '\u0417\u0430\u043f\u0438\u0441\u044c',
                'verbose_name_plural': '\u0417\u0430\u043f\u0438\u0441\u0438',
            },
        ),
    ]
