# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        s = """3	http://img-fotki.yandex.ru/get/6205/19044756.fd/0_83579_94da9a39_orig
10	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_8357a_c410775b_orig
11	http://img-fotki.yandex.ru/get/6001/19044756.ff/0_8362b_7da939c8_orig
16	http://img-fotki.yandex.ru/get/6000/19044756.fd/0_8357c_711a7cb2_orig
21	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835f9_390e43c4_orig
25	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_8357e_21e14769_orig
28	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_8357f_b6d4c006_orig
30	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_83581_396145d1_orig
31	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835fa_fbff976d_orig
35	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_83582_9f84c449_orig
42	http://img-fotki.yandex.ru/get/6205/19044756.fd/0_83584_35d371fe_orig
44	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835fb_9d09010c_orig
48	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_83586_816fb497_orig
50	http://img-fotki.yandex.ru/get/6000/19044756.fe/0_835fc_3e77ba17_orig
52	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_83587_7b6a3542_orig
55	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_83589_c2bed453_orig
56	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_8358a_80435bbe_orig
57	http://img-fotki.yandex.ru/get/6000/19044756.fd/0_8358c_af835850_orig
60	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_8358d_d408b816_orig
61	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835fe_772e6e1b_orig
64	http://img-fotki.yandex.ru/get/6001/19044756.fe/0_835ff_6cf6c0b0_orig
70	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_83600_21078de2_orig
73	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_8358f_e9d94084_orig
75	http://img-fotki.yandex.ru/get/6000/19044756.fd/0_83591_2adb8bb5_orig
76	http://img-fotki.yandex.ru/get/6001/19044756.fd/0_83593_592d3b3a_orig
77	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_83594_31ec740e_orig
81	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_83596_492e728e_orig
82	http://img-fotki.yandex.ru/get/6001/19044756.fe/0_83603_2a79eda4_orig
85	http://img-fotki.yandex.ru/get/6000/19044756.fe/0_83604_927bfa79_orig
88	http://img-fotki.yandex.ru/get/6205/19044756.ff/0_8362c_14a2132b_orig
102	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_83597_cc96c8a6_orig
105	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_83598_378ccfb7_orig
110	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_8359b_f78efc4e_orig
111	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_8359c_bc1795d7_orig
123	http://img-fotki.yandex.ru/get/6205/19044756.fd/0_8359d_ddbdd5a0_orig
125	http://img-fotki.yandex.ru/get/6001/19044756.fd/0_8359f_bfa8ae2d_orig
126	http://img-fotki.yandex.ru/get/6205/19044756.fd/0_835a0_f9610b2b_orig
130	http://img-fotki.yandex.ru/get/6001/19044756.fe/0_83605_197bd9b1_orig
131	http://img-fotki.yandex.ru/get/6205/19044756.ff/0_83606_4002d130_orig
139	http://img-fotki.yandex.ru/get/6000/19044756.ff/0_83608_a5a16a3_orig
140	http://img-fotki.yandex.ru/get/6205/19044756.ff/0_8362e_3a96a25b_orig
143	http://img-fotki.yandex.ru/get/6205/19044756.ff/0_83609_4d887b42_orig
144	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_835a2_3685b0c0_orig
145	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_835a3_89bd6faa_orig
147	http://img-fotki.yandex.ru/get/6000/19044756.fd/0_835a5_cfba2444_orig
153	http://img-fotki.yandex.ru/get/6104/19044756.fd/0_835a7_8cebae03_orig
154	http://img-fotki.yandex.ru/get/6204/19044756.fd/0_835a8_6de391f5_orig
196	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_835aa_3552f4cc_orig
201	http://img-fotki.yandex.ru/get/6001/19044756.fd/0_835ab_7c6b44cf_orig
202	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835ac_85f7e60f_orig
215	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835ae_b0b3c622_orig
243	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835b0_816a9541_orig
273	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835b1_6d2d9eb6_orig
274	http://img-fotki.yandex.ru/get/6001/19044756.fe/0_835b3_b6a10c9c_orig
277	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835b4_db62066a_orig
280	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835b6_96870867_orig
281	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835b7_80ad0706_orig
287	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835b8_2d475f27_orig
310	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835ba_d04317c3_orig
321	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835bc_9b4fbf4c_orig
332	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835be_27aefa4_orig
335	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835bf_46178ec4_orig
345	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835c1_4b841967_orig
346	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835c3_eed92532_orig
347	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835c5_7c21b7a_orig
349	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835c6_c202ef24_orig
358	http://img-fotki.yandex.ru/get/6000/19044756.fe/0_835c7_f8c2becf_orig
359	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835c9_661f98d2_orig
360	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835cc_adcbe60f_orig
361	http://img-fotki.yandex.ru/get/6000/19044756.fe/0_835cf_3cbb4bc_orig
362	http://img-fotki.yandex.ru/get/6001/19044756.fe/0_835d1_811b23c2_orig
364	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835d2_2fff6119_orig
383	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835d3_9d13fddd_orig
391	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835d5_a5f9b40c_orig
413	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835d6_becfc6e1_orig
455	http://img-fotki.yandex.ru/get/6105/19044756.fd/0_83567_b3cafe8c_orig
486	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835d7_7af96f8c_orig
489	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835da_e16c2093_orig
490	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835db_8b8afb75_orig
491	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835dc_f2d3038c_orig
492	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835de_853f3014_orig
532	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835df_5e3f689f_orig
1203	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835e0_ff1c85aa_orig
1239	http://img-fotki.yandex.ru/get/6105/19044756.fe/0_835e3_a63f510a_orig
1240	http://img-fotki.yandex.ru/get/6104/19044756.fe/0_835e4_e646d7b6_orig
1242	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835e5_6016cc85_orig
1243	http://img-fotki.yandex.ru/get/6001/19044756.fe/0_835e7_b13f197e_orig
1246	http://img-fotki.yandex.ru/get/6205/19044756.fe/0_835e8_23bc2508_orig
1250	http://img-fotki.yandex.ru/get/6204/19044756.fe/0_835eb_5dad1e49_orig
1257	http://img-fotki.yandex.ru/get/6000/19044756.fe/0_835ec_bfc21b70_orig
1334	http://img-fotki.yandex.ru/get/6000/19044756.fd/0_83575_37d91400_orig"""

        orm.Man.objects.all().update(image=None)

        for row in s.split("\n"):
            id, url = row.split()
            orm.Man.objects.filter(id=id).update(image=url.strip())



    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'core.discount': {
            'Meta': {'object_name': 'Discount'},
            'card': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contacts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.district': {
            'Meta': {'object_name': 'District'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'core.friend': {
            'Meta': {'unique_together': "(('user_a', 'user_b'),)", 'object_name': 'Friend'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'object'", 'to': "orm['auth.User']"}),
            'user_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject'", 'to': "orm['auth.User']"})
        },
        'core.itemvote': {
            'Meta': {'object_name': 'ItemVote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'manual'", 'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.man': {
            'Meta': {'object_name': 'Man'},
            'angles': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footsize': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('yafotki.fields.YFField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_photographer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_rider': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'primary_synonim': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'synonim'", 'null': 'True', 'to': "orm['core.Man']"}),
            'ridingsince': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sponsors': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'stance': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'core.man2movie': {
            'Meta': {'object_name': 'Man2Movie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'man': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Man']"}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Movie']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'actor'", 'max_length': '20'})
        },
        'core.mountain': {
            'Meta': {'object_name': 'Mountain'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.District']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'has_light': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_ratrack': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hotel': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Region']"}),
            'rental': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'room': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'root_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
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
        'core.mountainphoto': {
            'Meta': {'object_name': 'MountainPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'mountain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Mountain']"})
        },
        'core.movie': {
            'Meta': {'object_name': 'Movie'},
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cover': ('yafotki.fields.YFField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_movie': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_songs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'studio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Studio']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'torrent': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.news': {
            'Meta': {'object_name': 'News'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'})
        },
        'core.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '70'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photographer'", 'null': 'True', 'to': "orm['core.Man']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Post']", 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rider'", 'null': 'True', 'to': "orm['core.Man']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'tags_str': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'yandex_fotki_image_src': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'core.picturebox': {
            'Meta': {'object_name': 'PictureBox'},
            'action': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ask_for_answer_amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'best_answer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'post_best_answer'", 'null': 'True', 'to': "orm['core.Comment']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_date_finish': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'event_date_start': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'is_question': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '70'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Rubric']", 'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Skill']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'tags_str': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'post'", 'max_length': '15'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'core.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bindings': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'board': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'boots': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'clothes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'equip': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_moderator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mountains': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pic_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pub_post_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'riding_style': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'send_news': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stance': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'unread_comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'unread_news_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'core.redirect': {
            'Meta': {'object_name': 'Redirect'},
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'core.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'menu_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Rubric']", 'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Skill']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'core.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.song': {
            'Meta': {'ordering': "('movie', 'order')", 'object_name': 'Song'},
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Movie']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'performer': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.studio': {
            'Meta': {'object_name': 'Studio'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'core.tag': {
            'Meta': {'ordering': "['-type', '-size']", 'object_name': 'Tag'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'need_recalc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_tag'", 'null': 'True', 'to': "orm['core.Tag']"}),
            'posts': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'primary_synonim': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'synonim'", 'null': 'True', 'to': "orm['core.Tag']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'})
        },
        'core.tag2skill': {
            'Meta': {'object_name': 'Tag2Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Skill']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']"})
        },
        'core.usernews': {
            'Meta': {'object_name': 'UserNews'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['core.News']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.uservisitstat': {
            'Meta': {'object_name': 'UserVisitStat'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.word': {
            'Meta': {'object_name': 'Word'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'common'", 'max_length': '20'})
        }
    }

    complete_apps = ['core']
    symmetrical = True
