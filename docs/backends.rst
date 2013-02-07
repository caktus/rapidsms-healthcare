Storage Backend API
====================================

If the existing storage backends do not met your needs then you can write you own backend.
You may want to store data using a popular medical record system (OpenMRS, FreeMED) or
NoSQL database (CouchDB, MongoDB). Since applications interact with the storages though
the client API they will transparently work with your new storage.

.. note::

    This is an advanced use case and not necessary for most users or application
    developers.

The data passed to the backend will match the data described in the
:ref:`patient <PATIENT_DATA_MODEL>` and :ref:`provider <PROVIDER_DATA_MODEL>` data
model sections. Backend methods which return data should return dictionaries matching
this format as well.


Backend API
------------------------------------

Additional backends should extend from :py:class:`HealthcareStorage` which is
defined below:

.. class:: HealthcareStorage()

    .. method:: get_patient(id)

        Patient data should be fetched for the given ``id`` and returned as a dictionary. If
        the patient does not exist this method should return ``None``.

    .. method:: create_patient(data)

        A patient record should be created for given set of ``data`` given as a dictionary.
        The newly created patient record should be returned as a dictionary.

    .. method:: update_patient(id, data)

        Patient data for the given ``id`` should be updated with the ``data`` dictionary. ``data``
        may not be a full set of the patient fields. This method should return ``True`` if a patient
        was found and updated and ``False`` otherwise.

    .. method:: delete_patient(id)

        Patient data for the given ``id`` should be deleted. This method should return ``True`` if a patient
        was found and deleted and ``False`` otherwise.

    .. method:: get_provider(id)

        Provider data should be fetched for the given ``id`` and returned as a dictionary. If
        the provider does not exist this method should return ``None``.

    .. method:: create_provider(data)

        A provider record should be created for given set of ``data`` given as a dictionary.
        The newly created provider record should be returned as a dictionary.

    .. method:: update_provider(id, data)

        Provider data for the given ``id`` should be updated with the ``data`` dictionary. ``data``
        may not be a full set of the provider fields. This method should return ``True`` if a provider
        was found and updated and ``False`` otherwise.

    .. method:: delete_provider(id)

        Provider data for the given ``id`` should be deleted. This method should return ``True`` if a
        provider was found and deleted and ``False`` otherwise.


Testing the Backend
------------------------------------

There is a testing mixin ``BackendTestMixin`` in ``healthcare.tests.base`` which
runs through a set of compatibility tests for the backends. You simply need to
attach the path of the backend to the ``backend`` attribute.

.. code-block:: python

    from django.test import TestCase

    from healthcare.tests.base import BackendTestMixin


    class FancyBackendTestCase(BackendTestMixin, TestCase):
        backend = 'path.to.new.backend'