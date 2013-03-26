# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Patient'
        db.create_table(u'djhealth_patient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'A', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sex', self.gf('django.db.models.fields.CharField')(default=u'', max_length=1, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('death_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(default=u'', max_length=512, blank=True)),
        ))
        db.send_create_signal(u'djhealth', ['Patient'])

        # Adding model 'Provider'
        db.create_table(u'djhealth_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'A', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(default=u'', max_length=512, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms.Contact'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'djhealth', ['Provider'])

        # Adding model 'PatientID'
        db.create_table(u'djhealth_patientid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'A', max_length=1)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djhealth.Patient'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'djhealth', ['PatientID'])


    def backwards(self, orm):
        # Deleting model 'Patient'
        db.delete_table(u'djhealth_patient')

        # Deleting model 'Provider'
        db.delete_table(u'djhealth_provider')

        # Deleting model 'PatientID'
        db.delete_table(u'djhealth_patientid')


    models = {
        u'djhealth.patient': {
            'Meta': {'object_name': 'Patient'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '512', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '1', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'A'", 'max_length': '1'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'djhealth.patientid': {
            'Meta': {'object_name': 'PatientID'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djhealth.Patient']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'A'", 'max_length': '1'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'djhealth.provider': {
            'Meta': {'object_name': 'Provider'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rapidsms.Contact']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '512', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'A'", 'max_length': '1'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['djhealth']