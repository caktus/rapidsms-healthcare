from django.db import models
from django.utils.translation import ugettext_lazy as _



class AuditModelBase(models.Model):
    ACTIVE = 'A'
    INACTIVE = 'I'
    STATUS_CHOICES = (
        (ACTIVE, _(u"Active")),
        (INACTIVE, _(u"Inactive")),
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
        (MALE, _(u"Male")),
        (FEMALE, _(u"Female")),
    )

    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=512, blank=True, default=u'')  

    def __unicode__(self):
        return self.name


class Provider(AuditModelBase):
    "Storage model for basic provider/health care worker information."

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=512, blank=True, default=u'')

    def __unicode__(self):
        return self.name


class PatientID(AuditModelBase):
    "Identifier for patient/facility pair."

    TYPE_GENERATED = 'G'
    TYPE_ISSUED = 'I'
    TYPE_CHOICES = (
        (TYPE_GENERATED, _(u"Generated")),
        (TYPE_ISSUED , _(u"Issued")),
    )

    uid = models.CharField(max_length=255)
    uid_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    patient = models.ForeignKey(Patient)
    location = models.CharField(max_length=512)

    def __unicode__(self):
        return self.uid