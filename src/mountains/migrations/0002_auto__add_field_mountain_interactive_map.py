# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Mountain.interactive_map'
        db.add_column(u'mountains_mountain', 'interactive_map',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Mountain.interactive_map'
        db.delete_column(u'mountains_mountain', 'interactive_map')


    models = {
        u'mountains.district': {
            'Meta': {'object_name': 'District'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'mountains.mountain': {
            'Meta': {'object_name': 'Mountain'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mountains.District']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'has_light': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_ratrack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hotel': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'interactive_map': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lifts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'longest': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'newbie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nightwork': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'oldschool': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overfall': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'parking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pistelength': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pistes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prices': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'proof_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mountains.Region']"}),
            'rental': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'room': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'safe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'snowpark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'webcam': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'work_time': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'mountains.mountainphoto': {
            'Meta': {'object_name': 'MountainPhoto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('yafotki.fields.YFField', [], {'max_length': '255'}),
            'mountain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mountains.Mountain']"})
        },
        u'mountains.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['mountains']