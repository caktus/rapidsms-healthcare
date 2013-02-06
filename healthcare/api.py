"""
Healthcare API client.
"""
from __future__ import unicode_literals

from django.conf import settings

from .backends.base import get_backend
from .exceptions import PatientDoesNotExist, ProviderDoesNotExist


class CategoryWrapper(object):
    "Simple wrapper to translate a category (patient/provider) of backend calls."

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


class PatientWrapper(CategoryWrapper):
    "Wrapper around backend patient calls."

    def __init__(self, backend):
        super(PatientWrapper, self).__init__(backend, 'patient')

    def get(self, id, location=None):
        result = super(PatientWrapper, self).get(id, location=location)
        if result is None:
            raise PatientDoesNotExist("Patient ID {0} was not found".format(id))
        return result


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


STORAGE_BACKEND = getattr(settings, 'HEALTHCARE_STORAGE_BACKEND', 'healthcare.backends.django.DjangoStorage')


client = HealthcareAPI(STORAGE_BACKEND)