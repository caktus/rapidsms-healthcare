from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AuditModelBase(models.Model):
    ACTIVE = 'A'
    INACTIVE = 'I'
    STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (INACTIVE, _('Inactive')),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        abstract = True


class Patient(AuditModelBase):
    "Storage model for basic patient information."

    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        ('', ''),
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, default='')
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=512, blank=True, default='')

    def __unicode__(self):
        return self.name


class Provider(AuditModelBase):
    "Storage model for basic provider/health care worker information."

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=512, blank=True, default='')

    def __unicode__(self):
        return self.name


class PatientID(AuditModelBase):
    "Identifier for patient/facility pair."

    uid = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient)
    source = models.CharField(max_length=512)

    def __unicode__(self):
        return self.uid
