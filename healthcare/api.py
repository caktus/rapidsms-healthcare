"""
Healthcare API client.
"""

from django.conf import settings

from .backends.base import get_backend


class CategoryWrapper(object):
    "Simple wrapper to translate a category (patient/provider) of backend calls."

    def __init__(self, backend, category):
        self.backend, self.category = backend, category

    def get(self, id, **kwargs):
        method = getattr(self.backend, 'get_{category}'.format(category=self.category))
        result = method(id, **kwargs)
        if result is None:
            pass
        return result

    def create(self, **kwargs):
        method = getattr(self.backend, 'create_{category}'.format(category=self.category))
        result = method(kwargs)
        if result is None:
            pass
        return result

    def update(self, id, **kwargs):
        method = getattr(self.backend, 'update_{category}'.format(category=self.category))
        result = method(id, kwargs)
        return bool(result)


class HealthcareAPI(object):
    "API Client for accessing healthcare data via the configured backend."

    def __init__(self, backend):
        self.backend = get_backend(backend)
        self.patients = CategoryWrapper(self.backend, 'patient')
        self.providers = CategoryWrapper(self.backend, 'provider')


STORAGE_BACKEND = getattr(settings, 'HEALTHCARE_STORAGE_BACKEND', 'healthcare.backends.django.DjangoStorage')


client = HealthcareAPI(STORAGE_BACKEND)