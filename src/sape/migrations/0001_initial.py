# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'sape_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('txt', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('page', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'sape', ['Link'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'sape_link')


    models = {
        u'sape.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'txt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['sape']