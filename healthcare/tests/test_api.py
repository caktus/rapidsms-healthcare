from __future__ import unicode_literals

import datetime

from django.utils import unittest

from mock import patch

from ..api import HealthcareAPI
from ..backends import comparisons
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

    def test_filter_patients(self):
        "Translate API patient filter calls to the backend."
        today = datetime.date.today()
        with patch('healthcare.backends.dummy.DummyStorage.filter_patients') as filter_call:
            test_calls = (
                # Filter args, Expected backend call
                ({'name': 'Jane'}, [('name', comparisons.EQUAL, 'Jane')]),
                ({'name__like': 'Jane'}, [('name', comparisons.LIKE, 'Jane')]),
                ({'name__in': ('Jane', )}, [('name', comparisons.IN, ('Jane', ))]),
                ({'birth_date__lt': today}, [('birth_date', comparisons.LT, today)]),
                ({'birth_date__lte': today}, [('birth_date', comparisons.LTE, today)]),
                ({'birth_date__gt': today}, [('birth_date', comparisons.GT, today)]),
                ({'birth_date__gte': today}, [('birth_date', comparisons.GTE, today)]),
            )
            for kwargs, expected in test_calls:
                self.client.patients.filter(**kwargs)
                self.assertTrue(filter_call.called, "Backend filter_patients should be called.")
                args, _ = filter_call.call_args
                self.assertEqual(expected, *args)
                filter_call.reset_mock()

    def test_filter_providers(self):
        "Translate API provider filter calls to the backend."
        today = datetime.date.today()
        with patch('healthcare.backends.dummy.DummyStorage.filter_providers') as filter_call:
            test_calls = (
                # Filter args, Expected backend call
                ({'name': 'Jane'}, [('name', comparisons.EQUAL, 'Jane')]),
                ({'name__like': 'Jane'}, [('name', comparisons.LIKE, 'Jane')]),
                ({'name__in': ('Jane', )}, [('name', comparisons.IN, ('Jane', ))]),
                ({'created_date__lt': today}, [('created_date', comparisons.LT, today)]),
                ({'created_date__lte': today}, [('created_date', comparisons.LTE, today)]),
                ({'created_date__gt': today}, [('created_date', comparisons.GT, today)]),
                ({'created_date__gte': today}, [('created_date', comparisons.GTE, today)]),
            )
            for kwargs, expected in test_calls:
                self.client.providers.filter(**kwargs)
                self.assertTrue(filter_call.called, "Backend filter_providers should be called.")
                args, _ = filter_call.call_args
                self.assertEqual(expected, *args)
                filter_call.reset_mock()

    def test_link_patient(self):
        "Link a patient with an another ID with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.link_patient') as link:
            self.client.patients.link(123, 'abc', 'FOO')
            self.assertTrue(link.called, "Backend link_patient should be called.")

    def test_unlink_patient(self):
        "Unlink a patient with an another ID with the API client."
        with patch('healthcare.backends.dummy.DummyStorage.unlink_patient') as unlink:
            self.client.patients.unlink(123, 'abc', 'FOO')
            self.assertTrue(unlink.called, "Backend unlink_patient should be called.")

    def test_get_patient_for_source(self):
        "Get a patient by source id/name."
        with patch('healthcare.backends.dummy.DummyStorage.get_patient') as get:
            self.client.patients.get(123, source='ABC')
            self.assertTrue(get.called, "Backend get_patient should be called.")
            args, kwargs = get.call_args
            self.assertEqual(123, args[0])
            self.assertEqual('ABC', kwargs['source'])

    def test_get_missing_patient_for_source(self):
        "Try to get a patient by source id/name which doesn't exist."
        self.assertRaises(PatientDoesNotExist, self.client.patients.get, 123, source='ABC')