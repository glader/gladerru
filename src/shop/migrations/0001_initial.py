# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('shop_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'], null=True, blank=True)),
            ('show_sex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('amount_of_goods', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal('shop', ['Category'])

        # Adding model 'Brand'
        db.create_table('shop_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('shop', ['Brand'])

        # Adding model 'Item'
        db.create_table('shop_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Brand'])),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('shop', ['Item'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('shop_category')

        # Deleting model 'Brand'
        db.delete_table('shop_brand')

        # Deleting model 'Item'
        db.delete_table('shop_item')


    models = {
        'shop.brand': {
            'Meta': {'ordering': "['title']", 'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'shop.category': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Category'},
            'amount_of_goods': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Category']", 'null': 'True', 'blank': 'True'}),
            'show_sex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'shop.item': {
            'Meta': {'ordering': "['category', 'title']", 'object_name': 'Item'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['shop']
