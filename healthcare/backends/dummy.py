import uuid

from .base import HealthcareStorage


class DummyStorage(HealthcareStorage):
    "In-memory storage. This should only be used for testing."

    _patients = {}
    _providers = {}

    def get_patient(self, id, location=None):
        "Retrieve a patient record by ID."
        uid = id if location is None else u'{0}-{1}'.format(id, location)
        return self._patients.get(uid)

    def create_patient(self, data):
        "Create a patient record."
        uid = uuid.uuid4().int
        self._patients[uid] = data
        data['id'] = uid
        return data

    def update_patient(self, id, data):
        "Update a patient record by ID."
        if id in self._patients:
            self._patients[id].update(data)
            return True
        return False

    def get_provider(self, id):
        "Retrieve a provider record by ID."
        return self._providers.get(id)

    def create_provider(self, data):
        "Create a provider record."
        uid = uuid.uuid4().int
        self._providers[uid] = data
        data['id'] = uid
        return data

    def update_provider(self, id, data):
        "Update a provider record by ID."
        if id in self._providers:
            self._providers[id].update(data)
            return True
        return False