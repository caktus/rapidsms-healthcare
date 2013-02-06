from __future__ import absolute_import

from django.forms.models import model_to_dict
from django.utils.timezone import now

from ..base import HealthcareStorage
from .models import Patient, Provider, PatientID


class DjangoStorage(HealthcareStorage):

    def _patient_to_dict(self, patient):
        "Convert a Patient model to a dictionary."
        # Mapping of all fields
        # Might need additional translation of field names
        result = model_to_dict(patient)
        result['created_date'] = patient.created_date
        result['updated_date'] = patient.updated_date
        return result

    def _provider_to_dict(self, provider):
        "Convert a Provider model to a dictionary."
        # Mapping of all fields
        # Might need additional translation of field names
        result = model_to_dict(provider)
        result['created_date'] = provider.created_date
        result['updated_date'] = provider.updated_date
        return result

    def get_patient(self, id, location=None):
        "Retrieve a patient record by ID."
        if location is None:
            try:
                patient = Patient.objects.get(pk=id)
            except (ValueError, Patient.DoesNotExist):
                patient = None
        else:
            try:
                patient_id = PatientID.objects.all().select_related('patient').get(
                    uid=id, location_id=location
                )
            except (ValueError, PatientID.DoesNotExist):
                patient = None
            else:
                patient = patient_id.patient
        return self._patient_to_dict(patient) if patient is not None else None

    def create_patient(self, data):
        "Create a patient record."
        # FIXME: Might need additional translation of field names
        try:
            patient = Patient.objects.create(**data)
        except:
            # FIXME: Can we make this exception tighter?
            patient = None
        return self._patient_to_dict(patient) if patient is not None else None

    def update_patient(self, id, data):
        "Update a patient record by ID."
        # FIXME: Might need additional translation of field names
        # FIXME: Might need additional error handling
        try:
            data['updated_date'] = now()
            return Patient.objects.filter(pk=id).update(**data)
        except ValueError:
            return False

    def delete_patient(self, id):
        "Delete a patient record by ID."
        try:
            patient = Patient.objects.filter(pk=id)
        except ValueError:
            return False
        else:
            if patient.exists():
                patient.delete()
                return True
            return False

    def get_provider(self, id):
        "Retrieve a provider record by ID."
        try:
            provider = Provider.objects.get(pk=id)
        except (ValueError, Provider.DoesNotExist):
            provider = None
        return self._provider_to_dict(provider) if provider is not None else None

    def create_provider(self, data):
        "Create a provider record."
        # FIXME: Might need additional translation of field names
        try:
            provider = Provider.objects.create(**data)
        except:
            # FIXME: Can we make this exception tighter?
            provider = None
        return self._provider_to_dict(provider) if provider is not None else None

    def update_provider(self, id, data):
        "Update a provider record by ID."
        # FIXME: Might need additional translation of field names
        # FIXME: Might need additional error handling
        try:
            data['updated_date'] = now()
            return Provider.objects.filter(pk=id).update(**data)
        except ValueError:
            return False

    def delete_provider(self, id):
        "Delete a provider record by ID."
        try:
            provider = Provider.objects.filter(pk=id)
        except ValueError:
            return False
        else:
            if provider.exists():
                provider.delete()
                return True
            return False