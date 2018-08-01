# coding: utf-8

from django.db import models, migrations
import core.models
from django.conf import settings
import yafotki.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('content', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435', blank=True)),
                ('status', models.CharField(max_length=50, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='\u0421\u043a\u0440\u044b\u0442\u044b\u0439')),
                ('order', models.CharField(max_length=255, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a', blank=True)),
                ('local_url', models.CharField(default=b'', max_length=100, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('object_id', models.PositiveIntegerField()),
                ('ip', models.CharField(max_length=30, null=True, verbose_name='IP', blank=True)),
                ('author', models.ForeignKey(on_delete=models.DO_NOTHING, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=models.DO_NOTHING, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439',
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload', yafotki.fields.YFField(max_length=255, upload_to=b'gladerru')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=200, verbose_name='\u0421\u043b\u043e\u0432\u043e')),
                ('url', models.URLField(verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('type', models.CharField(default=b'manual', max_length=20, verbose_name='\u0422\u0438\u043f', choices=[(b'auto', '\u0418\u0437 \u0434\u0440\u0443\u0433\u043e\u0439 \u0442\u0430\u0431\u043b\u0438\u0446\u044b'), (b'manual', '\u0420\u0443\u043a\u0430\u043c\u0438')])),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043c\u0435\u043d\u0430',
                'verbose_name_plural': '\u0417\u0430\u043c\u0435\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.SlugField(max_length=255, verbose_name='\u0423\u0440\u043b')),
                ('order', models.PositiveIntegerField(default=100, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a')),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u043d\u043e\u0432\u043e\u0441\u0442\u0435\u0439',
                'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u043d\u043e\u0432\u043e\u0441\u0442\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=250, null=True, verbose_name='\u041a\u043e\u0434 \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438', blank=True)),
                ('title', models.CharField(max_length=250, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430', blank=True)),
                ('status', models.CharField(default=b'pub', max_length=50, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'pub', '\u041e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d\u043e'), (b'save', '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'), (b'deferred', '\u041e\u0442\u043b\u043e\u0436\u0435\u043d\u043e'), (b'del', '\u0423\u0434\u0430\u043b\u0435\u043d\u043e'), (b'ban', '\u0417\u0430\u0431\u0430\u043d\u0435\u043d\u043e'), (b'premoderate', '\u041f\u0440\u0435\u043c\u043e\u0434\u0435\u0440\u0430\u0446\u0438\u044f')])),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('place', models.CharField(max_length=250, null=True, verbose_name='\u041c\u0435\u0441\u0442\u043e', blank=True)),
                ('yandex_fotki_image_src', models.CharField(max_length=255, null=True, verbose_name='\u041f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435', blank=True)),
                ('rating', models.FloatField(default=0.0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('best', models.DateTimeField(null=True, verbose_name='\u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u043e\u0439', blank=True)),
                ('local_url', models.CharField(default=b'', max_length=70, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('author', models.ForeignKey(on_delete=models.DO_NOTHING, related_name='core_user', verbose_name='\u0410\u0432\u0442\u043e\u0440', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('photographer', models.ForeignKey(on_delete=models.DO_NOTHING, related_name='core_photographer', verbose_name='\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444', blank=True, to='movies.Man', null=True)),
            ],
            options={
                'verbose_name': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438',
            },
            bases=(models.Model, core.models.UIDMixin),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('title', models.CharField(max_length=250, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True)),
                ('slug', models.SlugField(default=None, max_length=255, blank=True, null=True, verbose_name='\u0423\u0440\u043b')),
                ('content', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435', blank=True)),
                ('status', models.CharField(default=b'save', max_length=50, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'pub', '\u041e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d\u043e'), (b'save', '\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'), (b'deferred', '\u041e\u0442\u043b\u043e\u0436\u0435\u043d\u043e'), (b'del', '\u0423\u0434\u0430\u043b\u0435\u043d\u043e'), (b'ban', '\u0417\u0430\u0431\u0430\u043d\u0435\u043d\u043e'), (b'premoderate', '\u041f\u0440\u0435\u043c\u043e\u0434\u0435\u0440\u0430\u0446\u0438\u044f')])),
                ('type', models.CharField(default=b'post', max_length=15, verbose_name='\u0422\u0438\u043f \u043f\u043e\u0441\u0442\u0430', choices=[(b'post', '\u041f\u043e\u0441\u0442'), (b'page', '\u0421\u0442\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430')])),
                ('abstract', models.TextField(null=True, verbose_name='\u0410\u043d\u043e\u043d\u0441', blank=True)),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0435\u0432', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='\u0421\u043a\u0440\u044b\u0442\u044b\u0439')),
                ('sticky_to', models.DateField(default=None, null=True, verbose_name='\u041f\u0440\u0438\u043a\u043b\u0435\u0435\u043d \u0434\u043e', blank=True)),
                ('icon', yafotki.fields.YFField(default=None, upload_to=b'gladerru', max_length=255, blank=True, null=True, verbose_name='\u0418\u043a\u043e\u043d\u043a\u0430')),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
                ('meta_keywords', models.TextField(default=None, help_text='meta-keywords', null=True, verbose_name='Keywords', blank=True)),
                ('author', models.ForeignKey(on_delete=models.DO_NOTHING, verbose_name='\u0410\u0432\u0442\u043e\u0440', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(on_delete=models.DO_NOTHING, default=None, blank=True, to='core.NewsCategory', null=True, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u0441\u0442',
                'verbose_name_plural': '\u041f\u043e\u0441\u0442\u044b',
            },
            bases=(models.Model, core.models.UIDMixin),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('content', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430', blank=True)),
                ('status', models.CharField(max_length=50, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', blank=True)),
                ('bindings', models.CharField(max_length=250, null=True, verbose_name='\u041a\u0440\u0435\u043f\u043b\u0435\u043d\u0438\u044f', blank=True)),
                ('birthday', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('board', models.CharField(max_length=250, null=True, verbose_name='\u0414\u043e\u0441\u043a\u0430', blank=True)),
                ('boots', models.CharField(max_length=250, null=True, verbose_name='\u0411\u043e\u0442\u0438\u043d\u043a\u0438', blank=True)),
                ('clothes', models.CharField(max_length=250, null=True, verbose_name='\u041e\u0434\u0435\u0436\u0434\u0430', blank=True)),
                ('city', models.CharField(max_length=250, null=True, verbose_name='\u0413\u043e\u0440\u043e\u0434', blank=True)),
                ('country', models.CharField(max_length=250, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', blank=True)),
                ('equip', models.CharField(max_length=250, null=True, verbose_name='\u0421\u043d\u0430\u0440\u044f\u0433\u0430', blank=True)),
                ('gender', models.CharField(default=b'', choices=[(b'm', '\u041c\u0430\u043b\u044c\u0447\u0438\u043a'), (b'f', '\u0414\u0435\u0432\u043e\u0447\u043a\u0430'), (b'', '\u041d\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u043b\u043e\u0441\u044c')], max_length=1, blank=True, null=True, verbose_name='\u041f\u043e\u043b')),
                ('icq', models.CharField(max_length=50, null=True, verbose_name='ICQ', blank=True)),
                ('interests', models.TextField(null=True, verbose_name='\u0418\u043d\u0442\u0435\u0440\u0435\u0441\u044b', blank=True)),
                ('is_moderator', models.BooleanField(default=False, verbose_name='\u042f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043c\u043e\u0434\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u043c')),
                ('last_visit', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u0437\u0430\u0445\u043e\u0434\u0430 \u043d\u0430 \u0441\u0430\u0439\u0442', blank=True)),
                ('mountains', models.CharField(max_length=250, null=True, verbose_name='\u0413\u043e\u0440\u044b', blank=True)),
                ('rating', models.FloatField(default=0.0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('riding_style', models.CharField(max_length=250, null=True, verbose_name='\u0421\u0442\u0438\u043b\u044c \u043a\u0430\u0442\u0430\u043d\u0438\u044f', blank=True)),
                ('stance', models.CharField(max_length=50, null=True, verbose_name='\u0421\u0442\u043e\u0439\u043a\u0430', blank=True)),
                ('referer', models.CharField(max_length=250, null=True, verbose_name='\u041e\u0442\u043a\u0443\u0434\u0430 \u043f\u0440\u0438\u0448\u0435\u043b', blank=True)),
                ('pic_count', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u0430\u0440\u0442\u0438\u043d\u043e\u043a')),
                ('pub_post_count', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u0441\u0442\u043e\u0432')),
                ('unread_news_count', models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043d\u0435\u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043d\u044b\u0445 \u0430\u043d\u043e\u043d\u0441\u043e\u0432')),
                ('send_news', models.BooleanField(default=True, verbose_name='\u041e\u0442\u0441\u044b\u043b\u0430\u0442\u044c \u043d\u043e\u0432\u043e\u0441\u0442\u0438 \u0441\u0430\u0439\u0442\u0430')),
                ('user', models.ForeignKey(on_delete=models.DO_NOTHING, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u0444\u0438\u043b\u044c',
                'verbose_name_plural': '\u041f\u0440\u043e\u0444\u0438\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=200, verbose_name='\u041e\u0442\u043a\u0443\u0434\u0430')),
                ('destination', models.CharField(max_length=200, verbose_name='\u041a\u0443\u0434\u0430')),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0434\u0438\u0440\u0435\u043a\u0442',
                'verbose_name_plural': '\u0420\u0435\u0434\u0438\u0440\u0435\u043a\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(max_length=200, verbose_name='\u041a\u043e\u0434')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('image', yafotki.fields.YFField(default=None, upload_to=b'gladerru', max_length=255, blank=True, null=True, verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430')),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': '\u0423\u043c\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0423\u043c\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u041a\u043e\u0434')),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('checked', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0440\u0435\u043d')),
                ('type', models.PositiveIntegerField(default=30, verbose_name='\u0422\u0438\u043f', choices=[(10, '\u0412\u0438\u0434 \u0441\u043f\u043e\u0440\u0442\u0430'), (20, '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f'), (30, '\u0422\u0435\u0433')])),
                ('size', models.PositiveIntegerField(default=0, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440')),
                ('posts', models.TextField(default=b'', verbose_name='\u041f\u043e\u0441\u0442\u044b')),
                ('need_recalc', models.BooleanField(default=False, verbose_name='\u0422\u0440\u0435\u0431\u0443\u0435\u0442 \u043f\u0435\u0440\u0435\u0441\u0447\u0435\u0442\u0430')),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
                ('category', models.ForeignKey(on_delete=models.DO_NOTHING, default=None, blank=True, to='core.NewsCategory', null=True, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f')),
                ('parent', models.ForeignKey(on_delete=models.DO_NOTHING, related_name='parent_tag', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True, to='core.Tag', null=True)),
                ('primary_synonim', models.ForeignKey(on_delete=models.DO_NOTHING, related_name='synonim', verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0441\u0438\u043d\u043e\u043d\u0438\u043c', blank=True, to='core.Tag', null=True)),
            ],
            options={
                'ordering': ['-type', '-size'],
                'verbose_name': '\u0422\u0435\u0433',
                'verbose_name_plural': '\u0422\u0435\u0433\u0438',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u0421\u043b\u043e\u0432\u043e')),
                ('slug', models.CharField(max_length=100, verbose_name='\u041a\u043e\u0434')),
                ('abstract', models.TextField(null=True, verbose_name='\u0412\u043a\u0440\u0430\u0442\u0446\u0435', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('meta_description', models.TextField(default=None, help_text='meta-description', null=True, verbose_name='Description', blank=True)),
                ('type', models.CharField(default=b'common', max_length=20, verbose_name='\u0421\u043b\u043e\u0432\u0430\u0440\u044c', choices=[(b'common', '\u041e\u0431\u0449\u0438\u0439 \u0441\u043b\u043e\u0432\u0430\u0440\u044c'), (b'jib', '\u0414\u0436\u0438\u0431\u0431\u0438\u043d\u0433'), (b'preparatory', '\u041f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435'), (b'grabs', '\u0413\u0440\u0435\u0431\u044b'), (b'spins', '\u0412\u0440\u0430\u0449\u0435\u043d\u0438\u044f'), (b'bigspins', '\u041f\u0440\u043e\u0434\u0432\u0438\u043d\u0443\u0442\u044b\u0435 \u0442\u0440\u044e\u043a\u0438'), (b'jibbing_tricks', '\u0414\u0436\u0438\u0431\u0431\u0438\u043d\u0433'), (b'pipe_tricks', '\u041f\u0430\u0439\u043f\u043e\u0432\u044b\u0435 \u043f\u0440\u044b\u0436\u043a\u0438'), (b'other_tricks', '\u0420\u0430\u0437\u043d\u043e\u0435')])),
            ],
            options={
                'verbose_name': '\u0421\u043b\u043e\u0432\u0430\u0440\u043d\u043e\u0435 \u0441\u043b\u043e\u0432\u043e',
                'verbose_name_plural': '\u0421\u043b\u043e\u0432\u0430\u0440\u043d\u044b\u0435 \u0441\u043b\u043e\u0432\u0430',
            },
            bases=(models.Model, core.models.UIDMixin),
        ),
        migrations.AddField(
            model_name='post',
            name='skill',
            field=models.ForeignKey(on_delete=models.DO_NOTHING, verbose_name='\u0423\u043c\u0435\u043d\u0438\u0435', blank=True, to='core.Skill', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', verbose_name='\u0422\u0435\u0433\u0438'),
        ),
        migrations.AddField(
            model_name='photo',
            name='post',
            field=models.ForeignKey(on_delete=models.DO_NOTHING, related_name='core_post', verbose_name='\u041f\u043e\u0441\u0442', blank=True, to='core.Post', null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='rider',
            field=models.ForeignKey(on_delete=models.DO_NOTHING, related_name='core_rider', verbose_name='\u0420\u0430\u0439\u0434\u0435\u0440', blank=True, to='movies.Man', null=True),
        ),
    ]
