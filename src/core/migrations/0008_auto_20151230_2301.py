# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151217_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='position',
            field=models.FloatField(blank=True, default=None, null=True, verbose_name='\u041f\u043e\u0437\u0438\u0446\u0438\u044f'),
        ),
    ]