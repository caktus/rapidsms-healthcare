import unittest

from mock import patch

from ..api import HealthcareAPI


class APIClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = HealthcareAPI('healthcare.backends.dummy.DummyStorage')

    def test_create_patient(self):
        "Create a new patient with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.create_patient') as create:
            self.client.patients.create(name='Joe', sex='M')
            self.assertTrue(create.called, "Backend create_patient should be called.")

    def test_get_patient(self):
        "Get a patient record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.get_patient') as create:
            self.client.patients.get(123)
            self.assertTrue(create.called, "Backend get_patient should be called.")

    def test_update_patient(self):
        "Update a patient record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.update_patient') as create:
            self.client.patients.update(123, name='Jane')
            self.assertTrue(create.called, "Backend update_patient should be called.")

    def test_create_provider(self):
        "Create a new provider with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.create_provider') as create:
            self.client.providers.create(name='Joe')
            self.assertTrue(create.called, "Backend create_provider should be called.")

    def test_get_provider(self):
        "Get a provider record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.get_provider') as create:
            self.client.providers.get(123)
            self.assertTrue(create.called, "Backend get_provider should be called.")

    def test_update_provider(self):
        "Update a provider record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.update_provider') as create:
            self.client.providers.update(123, name='Jane')
            self.assertTrue(create.called, "Backend update_provider should be called.")

    def test_invalid_category(self):
        "Attempt to access an invalid category."
        test = lambda: self.client.foobar
        self.assertRaises(AttributeError, test)

    def test_invalid_method(self):
        "Attempt to access an method for a given category."
        test = lambda: self.client.patients.foobar
        self.assertRaises(AttributeError, test)