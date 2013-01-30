"""
Healthcare API client.

from healthcare.api import client

patient = client.patients.get(123)
"""

from django.conf import settings
from django.utils import importlib

from .backends.base import InvalidBackendError


def get_backend(path):
    "Return a backend instance from the full Python path."
    try:
        # Trying to import the given backend
        mod_path, cls_name = path.rsplit('.', 1)
        mod = importlib.import_module(mod_path)
        backend_cls = getattr(mod, cls_name)
    except (AttributeError, ImportError, ValueError):
        raise InvalidBackendError("Could not find backend '%s'" % path)
    else:
        return backend_cls()


class CategoryWrapper(object):
    "Simple wrapper to translate a category (patient/provider) of backend calls."

    def __init__(self, backend, category):
        self.backend, self.category = client, category

    def __getattr__(self, name):
        method = getattr(self.backend, '{0}_{1}'.format(name, self.category))
        if method is None:
            raise AttributeError(name)
        return method


class HealthcareAPI(object):
    "API Client for accessing healthcare data via the configured backend."

    def __init__(self):
        name = getattr(settings, 'HEALTHCARE_STORAGE_BACKEND', 'healthcare.backends.django.DjangoStorage')
        self.backend = get_backend(name)
        self.patients = ResourceWrapper(self.backend, 'patient')
        self.providers = ResourceWrapper(self.backend, 'provider')


client = HealthcareAPI()