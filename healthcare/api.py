"""
Healthcare API client.

from healthcare.api import client

patient = client.patients.get(123)
"""

from django.conf import settings

from .backends.base import get_backend


class CategoryWrapper(object):
    "Simple wrapper to translate a category (patient/provider) of backend calls."

    def __init__(self, backend, category):
        self.backend, self.category = backend, category

    def __getattr__(self, name):
        method = getattr(self.backend, '{0}_{1}'.format(name, self.category), None)
        if method is None:
            raise AttributeError(name)
        return method


class HealthcareAPI(object):
    "API Client for accessing healthcare data via the configured backend."

    def __init__(self, backend):
        self.backend = get_backend(backend)
        self.patients = CategoryWrapper(self.backend, 'patient')
        self.providers = CategoryWrapper(self.backend, 'provider')


STORAGE_BACKEND = getattr(settings, 'HEALTHCARE_STORAGE_BACKEND', 'healthcare.backends.django.DjangoStorage')


client = HealthcareAPI(STORAGE_BACKEND)