# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Man'
        db.create_table(u'movies_man', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_rider', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_photographer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_director', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('angles', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('footsize', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
            ('image', self.gf('yafotki.fields.YFField')(default=None, max_length=255, null=True, blank=True)),
            ('ridingsince', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('sponsors', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('stance', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('primary_synonim', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='synonim', null=True, to=orm['movies.Man'])),
        ))
        db.send_create_signal(u'movies', ['Man'])

        # Adding model 'Studio'
        db.create_table(u'movies_studio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal(u'movies', ['Studio'])

        # Adding model 'Movie'
        db.create_table(u'movies_movie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('studio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movies.Studio'], null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('cover', self.gf('yafotki.fields.YFField')(default=None, max_length=255, null=True, blank=True)),
            ('torrent', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('teaser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('full_movie', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('has_songs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'movies', ['Movie'])

        # Adding model 'Man2Movie'
        db.create_table(u'movies_man2movie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('man', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movies.Man'])),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movies.Movie'])),
            ('role', self.gf('django.db.models.fields.CharField')(default='actor', max_length=20)),
        ))
        db.send_create_signal(u'movies', ['Man2Movie'])

        # Adding model 'Song'
        db.create_table(u'movies_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movies.Movie'])),
            ('performer', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'movies', ['Song'])

        # Adding model 'Photo'
        db.create_table(u'movies_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Post'], null=True, blank=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rider', null=True, to=orm['movies.Man'])),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photographer', null=True, to=orm['movies.Man'])),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('yandex_fotki_image_src', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('best', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('local_url', self.gf('django.db.models.fields.CharField')(default='', max_length=70)),
        ))
        db.send_create_signal(u'movies', ['Photo'])

        # Adding model 'PictureBox'
        db.create_table(u'movies_picturebox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movies.Photo'])),
            ('action', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'movies', ['PictureBox'])


    def backwards(self, orm):
        # Deleting model 'Man'
        db.delete_table(u'movies_man')

        # Deleting model 'Studio'
        db.delete_table(u'movies_studio')

        # Deleting model 'Movie'
        db.delete_table(u'movies_movie')

        # Deleting model 'Man2Movie'
        db.delete_table(u'movies_man2movie')

        # Deleting model 'Song'
        db.delete_table(u'movies_song')

        # Deleting model 'Photo'
        db.delete_table(u'movies_photo')

        # Deleting model 'PictureBox'
        db.delete_table(u'movies_picturebox')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.newscategory': {
            'Meta': {'object_name': 'NewsCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.post': {
            'Meta': {'object_name': 'Post'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['core.NewsCategory']", 'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_date_finish': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'event_date_start': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'item_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '70'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Rubric']", 'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Skill']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'tags_str': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'post'", 'max_length': '15'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'core.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('yafotki.fields.YFField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'menu_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Rubric']", 'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Skill']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'core.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'core.tag': {
            'Meta': {'ordering': "['-type', '-size']", 'object_name': 'Tag'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'need_recalc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_tag'", 'null': 'True', 'to': u"orm['core.Tag']"}),
            'posts': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'primary_synonim': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'synonim'", 'null': 'True', 'to': u"orm['core.Tag']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'})
        },
        u'movies.man': {
            'Meta': {'object_name': 'Man'},
            'angles': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footsize': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_photographer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_rider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'primary_synonim': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'synonim'", 'null': 'True', 'to': u"orm['movies.Man']"}),
            'ridingsince': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sponsors': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'stance': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'movies.man2movie': {
            'Meta': {'object_name': 'Man2Movie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'man': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['movies.Man']"}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['movies.Movie']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'actor'", 'max_length': '20'})
        },
        u'movies.movie': {
            'Meta': {'object_name': 'Movie'},
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cover': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_movie': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_songs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'studio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['movies.Studio']", 'null': 'True', 'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'torrent': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'movies.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '70'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photographer'", 'null': 'True', 'to': u"orm['movies.Man']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Post']", 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rider'", 'null': 'True', 'to': u"orm['movies.Man']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'yandex_fotki_image_src': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'movies.picturebox': {
            'Meta': {'object_name': 'PictureBox'},
            'action': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['movies.Photo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'movies.song': {
            'Meta': {'ordering': "('movie', 'order')", 'object_name': 'Song'},
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['movies.Movie']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'performer': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'movies.studio': {
            'Meta': {'object_name': 'Studio'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['movies']