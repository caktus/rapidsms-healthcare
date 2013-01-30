"""
Healthcare data storage backend API. All backends should extend from this base.
"""


class HealthcareStorage(object):

    def get_patient_record(self, id):
        "Retrieve a patient record by ID."
        raise NotImplementedError("Define in subclass")

    def create_patient_record(self, data=None):
        "Create a patient record."
        raise NotImplementedError("Define in subclass")

    def update_patient_record(self, id, data=None):
        "Update a patient record by ID."
        raise NotImplementedError("Define in subclass")

    def get_provider_record(self, id):
        "Retrieve a provider record by ID."
        raise NotImplementedError("Define in subclass")

    def create_provider_record(self, data=None):
        "Create a provider record."
        raise NotImplementedError("Define in subclass")

    def update_provider_record(self, id, data=None):
        "Update a provider record by ID."
        raise NotImplementedError("Define in subclass")
