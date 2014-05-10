# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table(u'mountains_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'mountains', ['Region'])

        # Adding model 'District'
        db.create_table(u'mountains_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'mountains', ['District'])

        # Adding model 'Mountain'
        db.create_table(u'mountains_mountain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mountains.District'], null=True, blank=True)),
            ('has_ratrack', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('yafotki.fields.YFField')(default=None, max_length=255, null=True, blank=True)),
            ('lifts', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('longest', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('nightwork', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('oldschool', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('overfall', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pistelength', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pistes', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('prices', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mountains.Region'])),
            ('service', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('snowpark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('webcam', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('work_time', self.gf('django.db.models.fields.TextField')(max_length=50, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('newbie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parking', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rental', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('room', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('safe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_service', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cafe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hotel', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('has_light', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_show', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('check_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('proof_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'mountains', ['Mountain'])

        # Adding model 'MountainPhoto'
        db.create_table(u'mountains_mountainphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mountain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mountains.Mountain'])),
            ('image', self.gf('yafotki.fields.YFField')(max_length=255)),
        ))
        db.send_create_signal(u'mountains', ['MountainPhoto'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table(u'mountains_region')

        # Deleting model 'District'
        db.delete_table(u'mountains_district')

        # Deleting model 'Mountain'
        db.delete_table(u'mountains_mountain')

        # Deleting model 'MountainPhoto'
        db.delete_table(u'mountains_mountainphoto')


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