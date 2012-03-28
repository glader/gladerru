# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        s = """1	http://img-fotki.yandex.ru/get/6001/19044756.102/0_83837_7809dcd2_orig
6	http://img-fotki.yandex.ru/get/6104/19044756.102/0_8383b_9e3d798d_orig
7	http://img-fotki.yandex.ru/get/6105/19044756.102/0_8383c_84da0011_orig
10	http://img-fotki.yandex.ru/get/6000/19044756.102/0_8383f_d75805c9_orig
13	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838d1_d3bc9a98_orig
14	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83842_172d453c_orig
15	http://img-fotki.yandex.ru/get/6000/19044756.104/0_838d2_6af41940_orig
16	http://img-fotki.yandex.ru/get/6105/19044756.102/0_83843_9429313_orig
17	http://img-fotki.yandex.ru/get/6105/19044756.104/0_838b6_fa75afc8_orig
18	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83844_10c35d1b_orig
19	http://img-fotki.yandex.ru/get/6104/19044756.104/0_838b7_54161132_orig
20	http://img-fotki.yandex.ru/get/6000/19044756.103/0_83890_85411c66_orig
21	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838d3_c1a7cdfa_orig
22	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83845_b644c308_orig
26	http://img-fotki.yandex.ru/get/6205/19044756.104/0_838b9_fc145120_orig
29	http://img-fotki.yandex.ru/get/6205/19044756.104/0_838bc_f36b7445_orig
31	http://img-fotki.yandex.ru/get/6205/19044756.102/0_8384c_43027019_orig
33	http://img-fotki.yandex.ru/get/6001/19044756.102/0_8384e_2fd1c76d_orig
34	http://img-fotki.yandex.ru/get/6001/19044756.102/0_8384f_a9462acc_orig
35	http://img-fotki.yandex.ru/get/6001/19044756.102/0_83850_b6e3bc0b_orig
36	http://img-fotki.yandex.ru/get/6105/19044756.104/0_838d4_eaf4c2ec_orig
37	http://img-fotki.yandex.ru/get/6001/19044756.102/0_83851_c4de2098_orig
38	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838d5_964bebcf_orig
39	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83852_af7f1e4f_orig
40	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83897_c9dc61c7_orig
41	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83853_97d82e76_orig
42	http://img-fotki.yandex.ru/get/6001/19044756.103/0_83898_c693dfa7_orig
43	http://img-fotki.yandex.ru/get/6205/19044756.102/0_83854_1d56c93a_orig
44	http://img-fotki.yandex.ru/get/6105/19044756.102/0_83855_baaebfbc_orig
45	http://img-fotki.yandex.ru/get/6000/19044756.102/0_83856_4f1b9b8c_orig
46	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83899_834e561e_orig
47	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83857_5af05ae9_orig
48	http://img-fotki.yandex.ru/get/6000/19044756.104/0_838be_30588de3_orig
49	http://img-fotki.yandex.ru/get/6001/19044756.102/0_83858_5c01961a_orig
50	http://img-fotki.yandex.ru/get/6105/19044756.102/0_83859_b0316b4e_orig
51	http://img-fotki.yandex.ru/get/6000/19044756.102/0_8385a_1c2fda75_orig
52	http://img-fotki.yandex.ru/get/6205/19044756.103/0_8389a_492e5aa3_orig
53	http://img-fotki.yandex.ru/get/6204/19044756.102/0_8385b_2e871918_orig
54	http://img-fotki.yandex.ru/get/6105/19044756.104/0_838d6_ea5becfd_orig
55	http://img-fotki.yandex.ru/get/6000/19044756.102/0_8385c_3db6e474_orig
57	http://img-fotki.yandex.ru/get/6104/19044756.102/0_8385e_890cdb2c_orig
59	http://img-fotki.yandex.ru/get/6205/19044756.102/0_8385f_2cf359bc_orig
60	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838c0_db9d7dbc_orig
61	http://img-fotki.yandex.ru/get/6000/19044756.104/0_838d7_9375d125_orig
63	http://img-fotki.yandex.ru/get/6204/19044756.102/0_83861_a385a01_orig
64	http://img-fotki.yandex.ru/get/6204/19044756.103/0_8389c_1bdc6c9_orig
65	http://img-fotki.yandex.ru/get/6000/19044756.103/0_8389d_32afa490_orig
66	http://img-fotki.yandex.ru/get/6205/19044756.102/0_83862_82d93eb_orig
67	http://img-fotki.yandex.ru/get/6105/19044756.102/0_83863_9c20ecfd_orig
68	http://img-fotki.yandex.ru/get/6001/19044756.103/0_8389e_120bf008_orig
69	http://img-fotki.yandex.ru/get/6205/19044756.102/0_83864_d3bde2cf_orig
70	http://img-fotki.yandex.ru/get/6001/19044756.102/0_83865_dfc0cfb2_orig
71	http://img-fotki.yandex.ru/get/6205/19044756.102/0_83866_483c89e5_orig
74	http://img-fotki.yandex.ru/get/6104/19044756.103/0_838a0_9945482d_orig
75	http://img-fotki.yandex.ru/get/6001/19044756.102/0_83869_d91d9149_orig
76	http://img-fotki.yandex.ru/get/6001/19044756.102/0_8386a_16fac3f5_orig
77	http://img-fotki.yandex.ru/get/6000/19044756.103/0_838a1_e983dbc8_orig
78	http://img-fotki.yandex.ru/get/6205/19044756.103/0_838a2_2a9734db_orig
79	http://img-fotki.yandex.ru/get/6000/19044756.104/0_838d8_88591e04_orig
80	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838c2_d3dfbebe_orig
81	http://img-fotki.yandex.ru/get/6105/19044756.103/0_838a3_1d56135a_orig
82	http://img-fotki.yandex.ru/get/6000/19044756.103/0_838a4_9e1e1d01_orig
83	http://img-fotki.yandex.ru/get/6105/19044756.103/0_838a5_5b690573_orig
84	http://img-fotki.yandex.ru/get/6001/19044756.103/0_838a6_2ce87b2b_orig
85	http://img-fotki.yandex.ru/get/6000/19044756.102/0_8386b_5b217ba2_orig
86	http://img-fotki.yandex.ru/get/6204/19044756.102/0_8386c_75f0f5d3_orig
87	http://img-fotki.yandex.ru/get/6205/19044756.103/0_8386d_2af1b836_orig
88	http://img-fotki.yandex.ru/get/6001/19044756.103/0_8386e_ad2c4bb3_orig
89	http://img-fotki.yandex.ru/get/6104/19044756.103/0_8386f_ade39a85_orig
90	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83870_89f5dbd9_orig
92	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838c3_710297c2_orig
93	http://img-fotki.yandex.ru/get/6104/19044756.103/0_838a8_958bd27b_orig
94	http://img-fotki.yandex.ru/get/6000/19044756.103/0_83871_7b8f4c5d_orig
95	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838c4_32d7f276_orig
99	http://img-fotki.yandex.ru/get/6205/19044756.104/0_838c8_f9cce61f_orig
100	http://img-fotki.yandex.ru/get/6000/19044756.103/0_83873_39505150_orig
101	http://img-fotki.yandex.ru/get/6000/19044756.103/0_83874_832c4a66_orig
103	http://img-fotki.yandex.ru/get/6205/19044756.103/0_83875_a68106b2_orig
104	http://img-fotki.yandex.ru/get/6105/19044756.103/0_838aa_e7ce54b0_orig
105	http://img-fotki.yandex.ru/get/6000/19044756.103/0_83876_5e033a86_orig
106	http://img-fotki.yandex.ru/get/6204/19044756.103/0_83877_98bbfd61_orig
107	http://img-fotki.yandex.ru/get/6000/19044756.104/0_838ca_ab8ebe86_orig
108	http://img-fotki.yandex.ru/get/6001/19044756.103/0_83878_a3ab5508_orig
109	http://img-fotki.yandex.ru/get/6105/19044756.103/0_838ab_f8dc389c_orig
110	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83879_3dafb32a_orig
111	http://img-fotki.yandex.ru/get/6105/19044756.103/0_8387a_4506e812_orig
112	http://img-fotki.yandex.ru/get/6104/19044756.103/0_8387b_b881d450_orig
113	http://img-fotki.yandex.ru/get/6205/19044756.103/0_8387c_23e2bf5d_orig
114	http://img-fotki.yandex.ru/get/6105/19044756.103/0_8387d_899cb8ea_orig
115	http://img-fotki.yandex.ru/get/6000/19044756.103/0_8387e_97d5fe9b_orig
116	http://img-fotki.yandex.ru/get/6105/19044756.103/0_838ac_e517224d_orig
117	http://img-fotki.yandex.ru/get/6000/19044756.103/0_8387f_5c587ade_orig
118	http://img-fotki.yandex.ru/get/6204/19044756.103/0_83880_cf094f40_orig
119	http://img-fotki.yandex.ru/get/6001/19044756.103/0_838ad_6502f23a_orig
120	http://img-fotki.yandex.ru/get/6204/19044756.103/0_83881_bdec095c_orig
121	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838cb_47da2a45_orig
122	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838cc_5c4b5aba_orig
123	http://img-fotki.yandex.ru/get/6205/19044756.104/0_838cd_62d83f8c_orig
124	http://img-fotki.yandex.ru/get/6001/19044756.103/0_83882_9793ad8b_orig
125	http://img-fotki.yandex.ru/get/6000/19044756.103/0_83883_e1970602_orig
126	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83884_c92d625c_orig
127	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83885_7f949f8a_orig
128	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83886_e747d926_orig
129	http://img-fotki.yandex.ru/get/6204/19044756.104/0_838ae_33ef9acf_orig
130	http://img-fotki.yandex.ru/get/6104/19044756.103/0_83887_268a24cd_orig
131	http://img-fotki.yandex.ru/get/6105/19044756.103/0_83888_741abd55_orig
132	http://img-fotki.yandex.ru/get/6204/19044756.103/0_83889_85ba9e22_orig
133	http://img-fotki.yandex.ru/get/6000/19044756.104/0_838af_565be79c_orig
134	http://img-fotki.yandex.ru/get/6001/19044756.103/0_8388a_3b9f6cb7_orig
135	http://img-fotki.yandex.ru/get/6000/19044756.103/0_8388b_53b15c99_orig"""

        orm.MountainPhoto.objects.all().update(image='')

        for row in s.split("\n"):
            id, url = row.split()
            orm.MountainPhoto.objects.filter(id=id).update(image=url.strip())

        orm.MountainPhoto.objects.filter(image='').delete()

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
            'image': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'image': ('yafotki.fields.YFField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'image': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
