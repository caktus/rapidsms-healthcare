import datetime
import operator

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
            (operator.eq, 'Joe', [patient]),
            (operator.mod, 'Jo', [patient]),
            (operator.mod, 'J', [patient, other_patient]),
            (operator.contains, ['Joe'], [patient]),
            (operator.contains, ['Joe', 'Jane'], [patient, other_patient]),
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
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M', 'birth_day': today})
        other_patient = self.backend.create_patient({'name': 'Jane', 'sex': 'F', 'birth_day': last_week})
        tests = (
            # Operator, Value, Expected
            (operator.lt, today, [other_patient]),
            (operator.lte, today, [patient, other_patient]),
            (operator.gt, today, []),
            (operator.gte, today, [patient]),
            (operator.eq, last_week, [other_patient]),
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
            (operator.eq, 'Joe', [provider]),
            (operator.mod, 'Jo', [provider]),
            (operator.mod, 'J', [provider, other_provider]),
            (operator.contains, ['Joe'], [provider]),
            (operator.contains, ['Joe', 'Jane'], [provider, other_provider]),
        )
        for op, val, expected in tests:
            result = self.backend.filter_providers(('name', op, val))
            self.assertItemsEqual(expected, result)