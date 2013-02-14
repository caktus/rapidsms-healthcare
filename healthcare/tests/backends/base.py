import datetime
import operator

from ...backends import comparisons
from ...backends.base import get_backend


class BackendTestMixin(object):
    "Common setup and tests for storage backends."

    backend = None

    def setUp(self):
        self.backend = get_backend(self.backend)

    def test_create_patient(self):
        "Store a new patient."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        # Newly create patients should have an id
        self.assertTrue(patient['id'])
        self.assertEqual(patient['created_date'].date(), datetime.date.today())
        self.assertTrue(patient['updated_date'].date(), datetime.date.today())

    def test_get_patient(self):
        "Retrive a stored patient."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        fetched = self.backend.get_patient(patient['id'])
        self.assertEqual(patient, fetched)

    def test_update_patient(self):
        "Update a field in the patient record."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        updated = patient['updated_date']
        result = self.backend.update_patient(patient['id'], {'name': 'Jane'})
        self.assertTrue(result)
        patient = self.backend.get_patient(patient['id'])
        self.assertEqual(patient['name'], 'Jane')
        self.assertTrue(patient['updated_date'] > updated)

    def test_get_missing_patient(self):
        "Backend should return None if the patient was not found."
        fetched = self.backend.get_patient('XXX')
        self.assertEqual(None, fetched)

    def test_update_missing_patient(self):
        "Backend should return a False value if no patient was found to update."
        result = self.backend.update_patient('XXX', {'name': 'Jane'})
        self.assertFalse(result)

    def test_delete_patient(self):
        "Delete an existing patient."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        result = self.backend.delete_patient(patient['id'])
        self.assertTrue(result)
        fetched = self.backend.get_patient(patient['id'])
        self.assertEqual(None, fetched)

    def test_delete_missing_patient(self):
        "Attempt to delete a patient which doesn't exist."
        result = self.backend.delete_patient('XXX')
        self.assertFalse(result)

    def test_create_provider(self):
        "Store a new provider."
        provider = self.backend.create_provider({'name': 'Joe'})
        # Newly create provider should have an id
        self.assertTrue(provider['id'])
        self.assertEqual(provider['created_date'].date(), datetime.date.today())
        self.assertTrue(provider['updated_date'].date(), datetime.date.today())

    def test_get_provider(self):
        "Retrive a stored provider."
        provider = self.backend.create_provider({'name': 'Joe'})
        fetched = self.backend.get_provider(provider['id'])
        self.assertEqual(provider, fetched)

    def test_update_provider(self):
        "Update a field in the provider record."
        provider = self.backend.create_provider({'name': 'Joe'})
        updated = provider['updated_date']
        result = self.backend.update_provider(provider['id'], {'name': 'Jane'})
        self.assertTrue(result)
        provider = self.backend.get_provider(provider['id'])
        self.assertEqual(provider['name'], 'Jane')
        self.assertTrue(provider['updated_date'] > updated)

    def test_get_missing_provider(self):
        "Backend should return None if the provider was not found."
        fetched = self.backend.get_provider('XXX')
        self.assertEqual(None, fetched)

    def test_update_missing_provider(self):
        "Backend should return a False value if no provider was found to update."
        result = self.backend.update_provider('XXX', {'name': 'Jane'})
        self.assertFalse(result)

    def test_delete_provider(self):
        "Delete an existing provider."
        provider = self.backend.create_provider({'name': 'Joe'})
        result = self.backend.delete_provider(provider['id'])
        self.assertTrue(result)
        fetched = self.backend.get_provider(provider['id'])
        self.assertEqual(None, fetched)

    def test_delete_missing_provider(self):
        "Attempt to delete a provider which doesn't exist."
        result = self.backend.delete_provider('XXX')
        self.assertFalse(result)

    def test_all_patients(self):
        "Get all patients with no filtering."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        other_patient = self.backend.create_patient({'name': 'Jane', 'sex': 'F'})
        result = self.backend.filter_patients()
        self.assertItemsEqual([patient, other_patient], result)

    def test_filter_patients_by_name(self):
        "Filter patients by common string expressions."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        other_patient = self.backend.create_patient({'name': 'Jane', 'sex': 'F'})
        tests = (
            # Operator, Value, Expected
            (comparisons.EQUAL, 'Joe', [patient]),
            (comparisons.LIKE, 'Jo', [patient]),
            (comparisons.LIKE, 'J', [patient, other_patient]),
            (comparisons.IN, ['Joe'], [patient]),
            (comparisons.IN, ['Joe', 'Jane'], [patient, other_patient]),
        )
        for op, val, expected in tests:
            result = self.backend.filter_patients(('name', op, val))
            self.assertItemsEqual(expected, result)

    def test_filter_patients_by_birth_date(self):
        "Filter patients by common date expressions."
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        last_week = today - datetime.timedelta(days=7)
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M', 'birth_date': today})
        other_patient = self.backend.create_patient({'name': 'Jane', 'sex': 'F', 'birth_date': last_week})
        tests = (
            # Operator, Value, Expected
            (comparisons.LT, today, [other_patient]),
            (comparisons.LTE, today, [patient, other_patient]),
            (comparisons.GT, today, []),
            (comparisons.GTE, today, [patient]),
            (comparisons.EQUAL, last_week, [other_patient]),
        )
        for op, val, expected in tests:
            result = self.backend.filter_patients(('birth_date', op, val))
            self.assertItemsEqual(expected, result)

    def test_all_providers(self):
        "Get all providers with no filtering."
        provider = self.backend.create_provider({'name': 'Joe'})
        other_provider = self.backend.create_provider({'name': 'Jane'})
        result = self.backend.filter_providers()
        self.assertItemsEqual([provider, other_provider], result)

    def test_filter_providers_by_name(self):
        "Filter providers by common string expressions."
        provider = self.backend.create_provider({'name': 'Joe'})
        other_provider = self.backend.create_provider({'name': 'Jane'})
        tests = (
            # Operator, Value, Expected
            (comparisons.EQUAL, 'Joe', [provider]),
            (comparisons.LIKE, 'Jo', [provider]),
            (comparisons.LIKE, 'J', [provider, other_provider]),
            (comparisons.IN, ['Joe'], [provider]),
            (comparisons.IN, ['Joe', 'Jane'], [provider, other_provider]),
        )
        for op, val, expected in tests:
            result = self.backend.filter_providers(('name', op, val))
            self.assertItemsEqual(expected, result)

    def test_link_patient_identifier(self):
        "Link a patient with an additional id."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        source_id = 'FOO'
        source_name = 'BAR'
        result = self.backend.link_patient(patient['id'], source_id, source_name)
        self.assertTrue(result, "Association should be created.")

    def test_link_missing_patient(self):
        "Try to link a patient which doesn't exist."
        source_id = 'FOO'
        source_name = 'BAR'
        result = self.backend.link_patient('XXXX', source_id, source_name)
        self.assertFalse(result, "Association should not be created.")

    def test_link_duplicate_id(self):
        "Try to associate multiple patients with the same id."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        other_patient = self.backend.create_patient({'name': 'Jane', 'sex': 'F'})
        source_id = 'FOO'
        source_name = 'BAR'
        self.backend.link_patient(patient['id'], source_id, source_name)
        result = self.backend.link_patient(other_patient['id'], source_id, source_name)
        self.assertFalse(result, "Association should not be created.")

    def test_unlink_patient_identifier(self):
        "Remove a patient identifier association."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        source_id = 'FOO'
        source_name = 'BAR'
        self.backend.link_patient(patient['id'], source_id, source_name)
        result = self.backend.unlink_patient(patient['id'], source_id, source_name)
        self.assertTrue(result, "Association should be removed.")

    def test_unlink_missing_patient(self):
        "Try to unlink a patient which doesn't exist."
        result = self.backend.unlink_patient(1234, 'XXXX', 'YYYYY')
        self.assertFalse(result, "Association should not be removed.")

    def test_unlink_missing_id(self):
        "Try to unlink an invalid id."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        source_id = 'FOO'
        source_name = 'BAR'
        self.backend.link_patient(patient['id'], source_id, source_name)
        result = self.backend.unlink_patient(patient['id'], 'XXXX', source_name)
        self.assertFalse(result, "Association should not be removed.")

    def test_get_by_source(self):
        "Get patient by source id/name pair."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        source_id = 'FOO'
        source_name = 'BAR'
        self.backend.link_patient(patient['id'], source_id, source_name)
        result = self.backend.get_patient(source_id, source=source_name)
        self.assertEqual(patient['id'], result['id'])

    def test_get_missing_by_source(self):
        "Try to get a patient for a missing source id/name pair."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        result = self.backend.get_patient('FOO', source='BAR')
        self.assertEqual(None, result)