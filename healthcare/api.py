"""
Healthcare API client.
"""
from __future__ import unicode_literals

import operator

from django.conf import settings

from .backends import comparisons
from .backends.base import get_backend

from .exceptions import PatientDoesNotExist, ProviderDoesNotExist


class CategoryWrapper(object):
    "Simple wrapper to translate a category (patient/provider) of backend calls."

    _lookup_mapping = {
        '': comparisons.EQUAL,
        'exact': comparisons.EQUAL,
        'like': comparisons.LIKE,
        'in': comparisons.IN,
        'lt': comparisons.LT,
        'lte': comparisons.LTE,
        'gt': comparisons.GT,
        'gte': comparisons.GTE,
    }

    def __init__(self, backend, category):
        self.backend, self.category = backend, category

    def get(self, id, **kwargs):
        method = getattr(self.backend, 'get_{category}'.format(category=self.category))
        return method(id, **kwargs)

    def create(self, **kwargs):
        method = getattr(self.backend, 'create_{category}'.format(category=self.category))
        return method(kwargs)

    def update(self, id, **kwargs):
        method = getattr(self.backend, 'update_{category}'.format(category=self.category))
        return bool(method(id, kwargs))

    def delete(self, id):
        method = getattr(self.backend, 'delete_{category}'.format(category=self.category))
        return bool(method(id))

    def _translate_filter_expression(self, name, value):
        "Convert a field lookup into the appropriate backend call."
        parts = name.split('__')
        if len(parts) > 1:
            field_name = parts[0]
            lookup = parts[-1]
        else:
            field_name = parts[0]
            lookup = ''
        comparison = self._lookup_mapping.get(lookup)
        if comparison is None:
            raise TypeError("Invalid lookup type: {0}".format(lookup))
        return (field_name, comparison, value)

    def filter(self, **kwargs):
        method = getattr(self.backend, 'filter_{category}s'.format(category=self.category))
        args = [self._translate_filter_expression(k, v) for k, v in kwargs.items()]
        return method(args)


class PatientWrapper(CategoryWrapper):
    "Wrapper around backend patient calls."

    def __init__(self, backend):
        super(PatientWrapper, self).__init__(backend, 'patient')

    def get(self, id, source=None):
        result = super(PatientWrapper, self).get(id, source=source)
        if result is None:
            if source:
                message = "Patient ID {0} for {1} was not found".format(id, source)
            else:
                message = "Patient ID {0} was not found".format(id)
            raise PatientDoesNotExist(message)
        return result

    def link(self, id, source_id, source_name):
        result = self.backend.link_patient(id, source_id, source_name)
        return bool(result)

    def unlink(self, id, source_id, source_name):
        result = self.backend.unlink_patient(id, source_id, source_name)
        return bool(result)


class ProviderWrapper(CategoryWrapper):
    "Wrapper around backend provider calls."

    def __init__(self, backend):
        super(ProviderWrapper, self).__init__(backend, 'provider')

    def get(self, id):
        result = super(ProviderWrapper, self).get(id)
        if result is None:
            raise ProviderDoesNotExist("Provider ID {0} was not found".format(id))
        return result


class HealthcareAPI(object):
    "API Client for accessing healthcare data via the configured backend."

    def __init__(self, backend):
        self.backend = get_backend(backend)
        self.patients = PatientWrapper(self.backend)
        self.providers = ProviderWrapper(self.backend)


STORAGE_BACKEND = getattr(settings, 'HEALTHCARE_STORAGE_BACKEND', 'healthcare.backends.djhealth.DjangoStorage')


client = HealthcareAPI(STORAGE_BACKEND)
