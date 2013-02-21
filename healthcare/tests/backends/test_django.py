from __future__ import absolute_import

from django.test import TestCase

from .base import BackendTestMixin


class DjangoBackendTestCase(BackendTestMixin, TestCase):
    backend = 'healthcare.backends.djhealth.DjangoStorage'