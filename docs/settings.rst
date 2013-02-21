Full Settings Reference
====================================

Below are the full set of settings for configuring rapidsms-healthcare along with
their default values.


.. _HEALTHCARE_STORAGE_BACKEND:

HEALTHCARE_STORAGE_BACKEND
------------------------------------

Default: ``'healthcare.backends.djhealth.DjangoStorage'``

Controls where rapidsms-healthcare stores patient and provider data. The default
backends provided are:

* :ref:`healthcare.backends.dummy.DummyStorage <DummyStorage>`
* :ref:`healthcare.backends.djhealth.DjangoStorage <DjangoStorage>`

Additional backends can be written as needed.