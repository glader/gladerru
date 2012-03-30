# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'ItemType'
        db.create_table('core_itemtype', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('core', ['ItemType'])

        # Adding model 'RelationType'
        db.create_table('core_relationtype', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('core', ['RelationType'])

        # Adding model 'Tag'
        db.create_table('core_tag', (
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_tag', blank=True, null=True, to=orm['core.Tag'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('primary_synonim', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonim', blank=True, null=True, to=orm['core.Tag'])),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Tag'])

        # Adding model 'Profile'
        db.create_table('core_profile', (
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('riding_style', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('last_visit', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('boots', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('equip', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('bindings', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('board', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('date_changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('icq', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('unread_post_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pic_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('mountains', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('stance', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('is_moderator', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('interests', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('favorites_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=1, null=True, blank=True)),
            ('unread_comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pub_post_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('avatar', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('clothes', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Profile'])

        # Adding model 'Skill'
        db.create_table('core_skill', (
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Skill'])

        # Adding model 'Tag2Skill'
        db.create_table('core_tag2skill', (
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Skill'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tag'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Tag2Skill'])

        # Adding model 'Comment'
        db.create_table('core_comment', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Comment'])

        # Adding model 'Item'
        db.create_table('core_item', (
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('torrent', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tags_str', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Skill'], null=True, blank=True)),
            ('best_answer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='best_answer', blank=True, null=True, to=orm['core.Comment'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('best', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('geography', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('date_changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ItemType'], null=True, blank=True)),
            ('image', self.gf('core.models.ThumbnailImageField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pub', max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ask_for_answer_amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('gallery_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=50, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('youtube', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rider', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('trick', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('menu_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_question', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Item'])

        # Adding M2M table for field favorites on 'Item'
        db.create_table('core_item_favorites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['core.item'], null=False)),
            ('profile', models.ForeignKey(orm['core.profile'], null=False))
        ))

        # Adding M2M table for field tags on 'Item'
        db.create_table('core_item_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['core.item'], null=False)),
            ('tag', models.ForeignKey(orm['core.tag'], null=False))
        ))

        # Adding model 'Relation'
        db.create_table('core_relation', (
            ('rel_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.RelationType'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item_b', self.gf('django.db.models.fields.related.ForeignKey')(related_name='b_relations', to=orm['core.Item'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_a', self.gf('django.db.models.fields.related.ForeignKey')(related_name='a_relations', to=orm['core.Item'])),
        ))
        db.send_create_signal('core', ['Relation'])

        # Adding model 'Letter'
        db.create_table('core_letter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Profile'])),
            ('date_sended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Letter'])

        # Adding model 'ItemVote'
        db.create_table('core_itemvote', (
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('vote', self.gf('django.db.models.fields.IntegerField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['ItemVote'])

        # Adding model 'UserVisit'
        db.create_table('core_uservisit', (
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_visits', to=orm['core.Item'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comments', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_visits', to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['UserVisit'])

        # Adding model 'Region'
        db.create_table('core_region', (
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('core', ['Region'])

        # Adding model 'District'
        db.create_table('core_district', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('core', ['District'])

        # Adding model 'Mountain'
        db.create_table('core_mountain', (
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('has_ratrack', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('service', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('oldschool', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nightwork', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pistelength', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.District'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('snow', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lifts', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('image', self.gf('core.models.ThumbnailImageField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pistes', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('work_time', self.gf('django.db.models.fields.TextField')(max_length=50, null=True, blank=True)),
            ('overfall', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('longest', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('prices', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('root_tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tag'], null=True, blank=True)),
            ('webcam', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('light', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Region'])),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('snowpark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Mountain'])

        # Adding model 'Man'
        db.create_table('core_man', (
            ('image', self.gf('core.models.ThumbnailImageField')(max_length=100, null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tag'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('ridingsince', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('primary_synonim', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonim', blank=True, null=True, to=orm['core.Man'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='pub', max_length=50)),
            ('stance', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sponsors', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('angles', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('is_rider', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('footsize', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
            ('is_director', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('is_photographer', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('core', ['Man'])

        # Adding model 'Studio'
        db.create_table('core_studio', (
            ('status', self.gf('django.db.models.fields.CharField')(default='pub', max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('core', ['Studio'])

        # Adding model 'Movie'
        db.create_table('core_movie', (
            ('status', self.gf('django.db.models.fields.CharField')(default='pub', max_length=50)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('torrent', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True)),
            ('cover', self.gf('core.models.ThumbnailImageField')(max_length=100, null=True, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('has_songs', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('teaser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Tag'], null=True, blank=True)),
            ('studio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Studio'], null=True, blank=True)),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('request_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Item'], null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('core', ['Movie'])

        # Adding M2M table for field favorites on 'Movie'
        db.create_table('core_movie_favorites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['core.movie'], null=False)),
            ('profile', models.ForeignKey(orm['core.profile'], null=False))
        ))

        # Adding model 'Man2Movie'
        db.create_table('core_man2movie', (
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Movie'])),
            ('role', self.gf('django.db.models.fields.CharField')(default='actor', max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('man', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Man'])),
        ))
        db.send_create_signal('core', ['Man2Movie'])

        # Adding model 'Photo'
        db.create_table('core_photo', (
            ('status', self.gf('django.db.models.fields.CharField')(default='pub', max_length=50)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('last_comment_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rider', blank=True, null=True, to=orm['core.Man'])),
            ('image', self.gf('core.models.ThumbnailImageField')(max_length=100, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photographer', blank=True, null=True, to=orm['core.Man'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Item'], null=True, blank=True)),
            ('tags_str', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('best', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Photo'])

        # Adding M2M table for field favorites on 'Photo'
        db.create_table('core_photo_favorites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm['core.photo'], null=False)),
            ('profile', models.ForeignKey(orm['core.profile'], null=False))
        ))

        # Adding M2M table for field tags on 'Photo'
        db.create_table('core_photo_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm['core.photo'], null=False)),
            ('tag', models.ForeignKey(orm['core.tag'], null=False))
        ))

        # Adding model 'Song'
        db.create_table('core_song', (
            ('performer', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Movie'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Song'])

        # Adding model 'Word'
        db.create_table('core_word', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='common', max_length=20)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Word'])

        # Adding model 'Discount'
        db.create_table('core_discount', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contacts', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Discount'])

        # Adding model 'VKontakteInvite'
        db.create_table('core_vkontakteinvite', (
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('core', ['VKontakteInvite'])

    def backwards(self, orm):

        # Deleting model 'ItemType'
        db.delete_table('core_itemtype')

        # Deleting model 'RelationType'
        db.delete_table('core_relationtype')

        # Deleting model 'Tag'
        db.delete_table('core_tag')

        # Deleting model 'Profile'
        db.delete_table('core_profile')

        # Deleting model 'Skill'
        db.delete_table('core_skill')

        # Deleting model 'Tag2Skill'
        db.delete_table('core_tag2skill')

        # Deleting model 'Comment'
        db.delete_table('core_comment')

        # Deleting model 'Item'
        db.delete_table('core_item')

        # Removing M2M table for field favorites on 'Item'
        db.delete_table('core_item_favorites')

        # Removing M2M table for field tags on 'Item'
        db.delete_table('core_item_tags')

        # Deleting model 'Relation'
        db.delete_table('core_relation')

        # Deleting model 'Letter'
        db.delete_table('core_letter')

        # Deleting model 'ItemVote'
        db.delete_table('core_itemvote')

        # Deleting model 'UserVisit'
        db.delete_table('core_uservisit')

        # Deleting model 'Region'
        db.delete_table('core_region')

        # Deleting model 'District'
        db.delete_table('core_district')

        # Deleting model 'Mountain'
        db.delete_table('core_mountain')

        # Deleting model 'Man'
        db.delete_table('core_man')

        # Deleting model 'Studio'
        db.delete_table('core_studio')

        # Deleting model 'Movie'
        db.delete_table('core_movie')

        # Removing M2M table for field favorites on 'Movie'
        db.delete_table('core_movie_favorites')

        # Deleting model 'Man2Movie'
        db.delete_table('core_man2movie')

        # Deleting model 'Photo'
        db.delete_table('core_photo')

        # Removing M2M table for field favorites on 'Photo'
        db.delete_table('core_photo_favorites')

        # Removing M2M table for field tags on 'Photo'
        db.delete_table('core_photo_tags')

        # Deleting model 'Song'
        db.delete_table('core_song')

        # Deleting model 'Word'
        db.delete_table('core_word')

        # Deleting model 'Discount'
        db.delete_table('core_discount')

        # Deleting model 'VKontakteInvite'
        db.delete_table('core_vkontakteinvite')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
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
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
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
        'core.item': {
            'Meta': {'object_name': 'Item'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ask_for_answer_amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'best_answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'best_answer'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Comment']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'favorites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Profile']", 'null': 'True', 'blank': 'True'}),
            'gallery_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geography': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('core.models.ThumbnailImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_question': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'menu_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rider': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Skill']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'tags_str': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'torrent': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'trick': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ItemType']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'youtube': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.itemtype': {
            'Meta': {'object_name': 'ItemType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'core.itemvote': {
            'Meta': {'object_name': 'ItemVote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.letter': {
            'Meta': {'object_name': 'Letter'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_sended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Profile']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.man': {
            'Meta': {'object_name': 'Man'},
            'angles': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footsize': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('core.models.ThumbnailImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_photographer': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_rider': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'primary_synonim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonim'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Man']"}),
            'ridingsince': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'sponsors': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'stance': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
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
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.District']", 'null': 'True', 'blank': 'True'}),
            'has_ratrack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('core.models.ThumbnailImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lifts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'light': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'longest': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'nightwork': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'oldschool': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'overfall': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pistelength': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pistes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prices': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Region']"}),
            'root_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'snow': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'snowpark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'webcam': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'work_time': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'core.movie': {
            'Meta': {'object_name': 'Movie'},
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cover': ('core.models.ThumbnailImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'favorites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Profile']", 'null': 'True', 'blank': 'True'}),
            'has_songs': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'request_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Item']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'studio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Studio']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'torrent': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'favorites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Profile']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('core.models.ThumbnailImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_comment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photographer'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Man']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Item']", 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rider'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Man']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'tags_str': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'core.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'favorites_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_moderator': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mountains': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pic_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pub_post_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'riding_style': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'stance': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'unread_comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'unread_post_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'core.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'core.relation': {
            'Meta': {'object_name': 'Relation'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'a_relations'", 'to': "orm['core.Item']"}),
            'item_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'b_relations'", 'to': "orm['core.Item']"}),
            'rel_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.RelationType']"})
        },
        'core.relationtype': {
            'Meta': {'object_name': 'RelationType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'Meta': {'object_name': 'Song'},
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pub'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'core.tag': {
            'Meta': {'object_name': 'Tag'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_tag'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Tag']"}),
            'primary_synonim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonim'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Tag']"}),
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
        'core.uservisit': {
            'Meta': {'object_name': 'UserVisit'},
            'comments': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_visits'", 'to': "orm['core.Item']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_visits'", 'to': "orm['auth.User']"})
        },
        'core.vkontakteinvite': {
            'Meta': {'object_name': 'VKontakteInvite'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'core.word': {
            'Meta': {'object_name': 'Word'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'common'", 'max_length': '20'})
        }
    }

    complete_apps = ['core']
