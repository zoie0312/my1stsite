# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table(u'infoholic_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'infoholic', ['Feed'])

        # Adding M2M table for field owners on 'Feed'
        db.create_table(u'infoholic_feed_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm[u'infoholic.feed'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'infoholic_feed_owners', ['feed_id', 'user_id'])

        # Adding model 'Category'
        db.create_table(u'infoholic_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'infoholic', ['Category'])

        # Adding M2M table for field owners on 'Category'
        db.create_table(u'infoholic_category_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'infoholic.category'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'infoholic_category_owners', ['category_id', 'user_id'])

        # Adding M2M table for field feeds on 'Category'
        db.create_table(u'infoholic_category_feeds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'infoholic.category'], null=False)),
            ('feed', models.ForeignKey(orm[u'infoholic.feed'], null=False))
        ))
        db.create_unique(u'infoholic_category_feeds', ['category_id', 'feed_id'])

        # Adding model 'Article'
        db.create_table(u'infoholic_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fetched_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('readed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('link', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['auth.User'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['infoholic.Feed'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['infoholic.Category'])),
        ))
        db.send_create_signal(u'infoholic', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table(u'infoholic_feed')

        # Removing M2M table for field owners on 'Feed'
        db.delete_table('infoholic_feed_owners')

        # Deleting model 'Category'
        db.delete_table(u'infoholic_category')

        # Removing M2M table for field owners on 'Category'
        db.delete_table('infoholic_category_owners')

        # Removing M2M table for field feeds on 'Category'
        db.delete_table('infoholic_category_feeds')

        # Deleting model 'Article'
        db.delete_table(u'infoholic_article')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'infoholic.article': {
            'Meta': {'ordering': "['-fetched_at', 'title']", 'object_name': 'Article'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['infoholic.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'fetched_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'readed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['infoholic.Feed']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'infoholic.category': {
            'Meta': {'ordering': "['created_at', 'name']", 'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['infoholic.Feed']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'infoholic.feed': {
            'Meta': {'ordering': "['created_at', 'title']", 'object_name': 'Feed'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['infoholic']