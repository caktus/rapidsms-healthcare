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

    .. method:: get_patient(id, source=None)

        Patient data should be fetched for the given ``id`` and returned as a dictionary. If
        the patient does not exist this method should return ``None``.

        ``source`` is an optional paramter. If given then the ``id`` should be interpreted
        as the ``source_id`` and the ``source`` as the ``source_name`` to find the patient
        using the association created by py:meth:`HealthcareStorage.link_patient`. If the patient
        cannot be found for this association it should also return ``None``.

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

    .. method:: filter_patients(*lookups)

        Returns a list of patients matching the set of lookups. If no patients were found it should
        return an empty list. If no lookups were passed it should return all patients. The details
        of the lookup structure is given in the next section. When multiple lookups are passed,
        the intersection of the results should be returned (default to AND the expressions).

    .. method:: link_patient(id, source_id, source_name)

        Associates a patient with an addition identifier. The ``source_id`` and ``source_name`` pair
        should be enforced as unique. This should return a ``True`` value if the association was created.
        Otherwise it should return ``False``.

    .. method:: unlink_patient(id, source_id, source_name)

        Removes an association of a patient with an addition identifier. This should return a ``True``
        value if the association was found and removed. Otherwise it should return ``False``.

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

    .. method:: filter_providers(*lookups)

        Returns a list of providers matching the set of lookups. If no providers were found it should
        return an empty list. If no lookups were passed it should return all providers. The details
        of the lookup structure is given in the next section. When multiple lookups are passed,
        the intersection of the results should be returned (default to AND the expressions).


Backend Lookups
------------------------------------

The above :py:meth:`HealthcareStorage.filter_patients` and py:meth:`HealthcareStorage.filter_providers`
methods are each passed a list of lookups for filtering the underlying records. Each of these
lookups is a 3-tuple ``(field_name, operator, value)``. The ``field_name`` is passed as a string
and must match a field name on the corresponding data model. The ``value`` is the requested value for
comparison which should be a standard Python type (int, float, list, sting, date, datetime, etc). The
``operator`` is one of the below constants from the ``healthcare.backends.comparisons`` module.

================================    ==============
Operator                            Comparison
================================    ==============
``EQUAL``                           Field is an exact match to the value
``LIKE``                            Field contains the value
``IN``                              Field is an exact match to one of the values in the value (list/tuple)
``LT``                              Field is less than the value
``LTE``                             Field is less than or equal to the value
``GT``                              Field is greater than the value
``GTE``                             Field is greater than or equal to the value
================================    ==============

The backend is responsible for mapping these operators to the meaningful expressions for its
storage method.


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

This should not be considered an complete set of tests and the developers should
write additional tests to cover edge cases in their backend.
