import datetime

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