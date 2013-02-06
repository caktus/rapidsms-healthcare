import unittest

from mock import patch

from ..api import HealthcareAPI
from ..exceptions import PatientDoesNotExist, ProviderDoesNotExist


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
        with patch('healthcare.backends.dummy.DummyStorage.get_patient') as get:
            self.client.patients.get(123)
            self.assertTrue(get.called, "Backend get_patient should be called.")

    def test_update_patient(self):
        "Update a patient record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.update_patient') as update:
            self.client.patients.update(123, name='Jane')
            self.assertTrue(update.called, "Backend update_patient should be called.")

    def test_delete_patient(self):
        "Delete a patient record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.delete_patient') as delete:
            self.client.patients.delete(123)
            self.assertTrue(delete.called, "Backend delete_patient should be called.")

    def test_create_provider(self):
        "Create a new provider with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.create_provider') as create:
            self.client.providers.create(name='Joe')
            self.assertTrue(create.called, "Backend create_provider should be called.")

    def test_get_provider(self):
        "Get a provider record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.get_provider') as get:
            self.client.providers.get(123)
            self.assertTrue(get.called, "Backend get_provider should be called.")

    def test_update_provider(self):
        "Update a provider record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.update_provider') as update:
            self.client.providers.update(123, name='Jane')
            self.assertTrue(update.called, "Backend update_provider should be called.")

    def test_delete_provider(self):
        "Delete a provide record with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.delete_provider') as delete:
            self.client.providers.delete(123)
            self.assertTrue(delete.called, "Backend delete_provider should be called.")

    def test_invalid_category(self):
        "Attempt to access an invalid category."
        test = lambda: self.client.foobar
        self.assertRaises(AttributeError, test)

    def test_invalid_method(self):
        "Attempt to access an method for a given category."
        test = lambda: self.client.patients.foobar
        self.assertRaises(AttributeError, test)

    def test_get_missing_patient(self):
        "Try to get a patient which doesn't exist."
        self.assertRaises(PatientDoesNotExist, self.client.patients.get, 123)

    def test_get_missing_provider(self):
        "Try to get a provider which doesn't exist."
        self.assertRaises(ProviderDoesNotExist, self.client.providers.get, 123)

    def test_update_missing_patient(self):
        "Try to update a patient which doesn't exist."
        self.assertFalse(self.client.patients.update(123, name='Jane'))

    def test_update_missing_provider(self):
        "Try to update a provider which doesn't exist."
        self.assertFalse(self.client.providers.update(123, name='Jane'))

    def test_delete_missing_patient(self):
        "Try to delete a patient which doesn't exist."
        self.assertFalse(self.client.patients.delete(123))

    def test_delete_missing_provider(self):
        "Try to delete a provider which doesn't exist."
        self.assertFalse(self.client.providers.delete(123))