# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table(u'github_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('client_secret', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('callback_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('default_scope', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'github', ['Application'])

        # Adding model 'Authentication'
        db.create_table(u'github_authentication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['github.Application'])),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, db_index=True)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'github', ['Authentication'])

        # Adding model 'User'
        db.create_table(u'github_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['github.Application'])),
            ('avatar_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'github', ['User'])

        # Adding unique constraint on 'User', fields ['uid', 'application']
        db.create_unique(u'github_user', ['uid', 'application_id'])

        # Adding model 'Repository'
        db.create_table(u'github_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='repositories', to=orm['github.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fork', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('html_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('clone_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('git_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ssh_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('svn_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('mirror_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('forks', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('forks_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('watchers', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('watchers_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('master_branch', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('open_issues', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('pushed_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'github', ['Repository'])

        # Adding unique constraint on 'Repository', fields ['uid', 'owner']
        db.create_unique(u'github_repository', ['uid', 'owner_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repository', fields ['uid', 'owner']
        db.delete_unique(u'github_repository', ['uid', 'owner_id'])

        # Removing unique constraint on 'User', fields ['uid', 'application']
        db.delete_unique(u'github_user', ['uid', 'application_id'])

        # Deleting model 'Application'
        db.delete_table(u'github_application')

        # Deleting model 'Authentication'
        db.delete_table(u'github_authentication')

        # Deleting model 'User'
        db.delete_table(u'github_user')

        # Deleting model 'Repository'
        db.delete_table(u'github_repository')


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
        u'github.application': {
            'Meta': {'object_name': 'Application'},
            'callback_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'client_secret': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'default_scope': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'github.authentication': {
            'Meta': {'object_name': 'Authentication'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['github.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'github.repository': {
            'Meta': {'unique_together': "(('uid', 'owner'),)", 'object_name': 'Repository'},
            'clone_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fork': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forks': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'forks_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'git_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'html_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'master_branch': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mirror_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'open_issues': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repositories'", 'to': u"orm['github.User']"}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pushed_at': ('django.db.models.fields.DateTimeField', [], {}),
            'size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'ssh_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'svn_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'watchers': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'watchers_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'github.user': {
            'Meta': {'unique_together': "(('uid', 'application'),)", 'object_name': 'User'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['github.Application']"}),
            'avatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['github']