"""
Healthcare data storage backend API. All backends should extend from this base.
"""


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
