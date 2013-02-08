from __future__ import absolute_import

import operator
import uuid

from django.utils.timezone import now

from . import comparisons
from .base import HealthcareStorage


class DummyStorage(HealthcareStorage):
    "In-memory storage. This should only be used for testing."

    _patients = {}
    _providers = {}

    _comparison_mapping = {
        comparisons.EQUAL: operator.eq,
        # operator.contains reverses the operands
        # http://docs.python.org/2/library/operator.html#operator.contains
        # field_value contains value
        comparisons.LIKE: operator.contains,
        # value contains field_value
        comparisons.IN: lambda a, b: operator.contains(b, a),
        comparisons.LT: operator.lt,
        comparisons.LTE: operator.le,
        comparisons.GT: operator.gt,
        comparisons.GTE: operator.ge,
    }

    def _lookup_to_filter(self, lookup):
        def filter_func(item):
            field, operator, value = lookup
            comparison_func = self._comparison_mapping[operator]
            field_value = item.get(field)
            if field_value is None:
                return False
            return comparison_func(field_value, value)
        return filter_func

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

    def filter_patients(self, *lookups):
        "Find patient records matching the given lookups."
        filters = map(self._lookup_to_filter, lookups)
        return filter(lambda t: all(f(t) for f in filters), self._patients.values())

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

    def filter_providers(self, *lookups):
        "Find provider records matching the given lookups."
        filters = map(self._lookup_to_filter, lookups)
        return filter(lambda t: all(f(t) for f in filters), self._providers.values())