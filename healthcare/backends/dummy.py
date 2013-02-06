from __future__ import absolute_import

import uuid

from django.utils.timezone import now

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
        data['created_date'] = now()
        data['updated_date'] = now()
        if 'status' not in data:
            data['status'] = 'A'
        self._patients[uid] = data
        data['id'] = uid
        return data

    def update_patient(self, id, data):
        "Update a patient record by ID."
        if id in self._patients:
            data['updated_date'] = now()
            self._patients[id].update(data)
            return True
        return False

    def delete_patient(self, id):
        "Delete a patient record by ID."
        if id in self._patients:
            del self._patients[id]
            return True
        return False

    def get_provider(self, id):
        "Retrieve a provider record by ID."
        return self._providers.get(id)

    def create_provider(self, data):
        "Create a provider record."
        uid = uuid.uuid4().int
        data['created_date'] = now()
        data['updated_date'] = now()
        if 'status' not in data:
            data['status'] = 'A'
        self._providers[uid] = data
        data['id'] = uid
        return data

    def update_provider(self, id, data):
        "Update a provider record by ID."
        if id in self._providers:
            data['updated_date'] = now()
            self._providers[id].update(data)
            return True
        return False

    def delete_provider(self, id):
        "Delete a provider record by ID."
        if id in self._providers:
            del self._providers[id]
            return True
        return False