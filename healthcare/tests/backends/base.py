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

    def test_get_patient(self):
        "Retrive a stored patient."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        fetched = self.backend.get_patient(patient['id'])
        self.assertEqual(patient, fetched)

    def test_update_patient(self):
        "Update a field in the patient record."
        patient = self.backend.create_patient({'name': 'Joe', 'sex': 'M'})
        self.backend.update_patient(patient['id'], {'name': 'Jane'})
        patient = self.backend.get_patient(patient['id'])
        self.assertEqual(patient['name'], 'Jane')