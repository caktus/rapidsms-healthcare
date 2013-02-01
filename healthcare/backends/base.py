"""
Healthcare data storage backend API. All backends should extend from this base.
"""
from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib


class InvalidBackendError(ImproperlyConfigured):
    pass


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


class HealthcareStorage(object):

    def get_patient(self, id, location=None):
        "Retrieve a patient record by ID."
        raise NotImplementedError("Define in subclass")

    def create_patient(self, data):
        "Create a patient record."
        raise NotImplementedError("Define in subclass")

    def update_patient(self, id, data):
        "Update a patient record by ID."
        raise NotImplementedError("Define in subclass")

    def get_provider(self, id):
        "Retrieve a provider record by ID."
        raise NotImplementedError("Define in subclass")

    def create_provider(self, data):
        "Create a provider record."
        raise NotImplementedError("Define in subclass")

    def update_provider(self, id, data):
        "Update a provider record by ID."
        raise NotImplementedError("Define in subclass")
