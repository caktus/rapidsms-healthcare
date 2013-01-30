import unittest

from .base import BackendTestMixin


class DummyBackendTestCase(BackendTestMixin, unittest.TestCase):
    backend = 'healthcare.backends.dummy.DummyStorage'