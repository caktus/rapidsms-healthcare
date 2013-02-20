from django.utils import unittest

from .base import BackendTestMixin


class DummyBackendTestCase(BackendTestMixin, unittest.TestCase):
    backend = 'healthcare.backends.dummy.DummyStorage'

    def setUp(self):
        super(DummyBackendTestCase, self).setUp()
        self.backend._patients = {}
        self.backend._providers = {}
        self.backend._patient_ids = {}