# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Photo.rating'
        db.delete_column(u'movies_photo', 'rating')

        # Deleting field 'Photo.post'
        db.delete_column(u'movies_photo', 'post_id')

        # Deleting field 'Photo.best'
        db.delete_column(u'movies_photo', 'best')

        # Deleting field 'Photo.author'
        db.delete_column(u'movies_photo', 'author_id')

        # Deleting field 'Photo.slug'
        db.delete_column(u'movies_photo', 'slug')

        # Deleting field 'Photo.content'
        db.delete_column(u'movies_photo', 'content')

        # Deleting field 'Photo.place'
        db.delete_column(u'movies_photo', 'place')

        # Deleting field 'Photo.local_url'
        db.delete_column(u'movies_photo', 'local_url')


    def backwards(self, orm):
        # Adding field 'Photo.rating'
        db.add_column(u'movies_photo', 'rating',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Photo.post'
        db.add_column(u'movies_photo', 'post',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Post'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.best'
        db.add_column(u'movies_photo', 'best',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.author'
        db.add_column(u'movies_photo', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.slug'
        db.add_column(u'movies_photo', 'slug',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.content'
        db.add_column(u'movies_photo', 'content',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.place'
        db.add_column(u'movies_photo', 'place',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.local_url'
        db.add_column(u'movies_photo', 'local_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=70),
                      keep_default=False)


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photographer'", 'null': 'True', 'to': u"orm['movies.Man']"}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rider'", 'null': 'True', 'to': u"orm['movies.Man']"}),
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