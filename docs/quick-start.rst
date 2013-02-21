Getting Started
====================================

Here you will find the necessary steps to install and initial configure the
rapidsms-healthcare application.


Requirements
------------------------------------

rapidsms-healthcare requires Python 2.6 or 2.7. Python 3 is not currently supported but is
planned in the future as Django and RapidSMS support for Python 3 increases. It also requires
the following packages:

* Django >= 1.4
* RapidSMS >= 0.11.0


Installation
------------------------------------

Stable releases of rapidsms-healthcare can be found on `PyPi <http://pypi.python.org/>`_
and `pip <http://www.pip-installer.org/>`_ is the recommended method for installing the package::

    pip install rapidsms-healthcare


Configuration
------------------------------------

The storage and retrieval of healthcare related data is configured by the :ref:`HEALTHCARE_STORAGE_BACKEND` setting.
If you are using the default storage backend you need to change your ``INSTALLED_APPS`` to include::

    INSTALLED_APPS = (
        # Other apps go here
        'healthcare.backends.djhealth',
    )

If you are using a different backend then you can skip this step. The Django backend uses `South <http://south.aeracode.org/>`_
to manage possible future changes to the schema. While not required if you are using South in your project
then you can create the tables needed for the backend via::

    python manage.py migrate djhealth

If you are not using South then you can create the tables via::

    python manage.py syncdb

.. note::

    While using South is optional, it is highly recommended. If you are not using South then you may need to
    apply future schema change yourself. When needed these will be noted in the release notes.


Next Steps
------------------------------------

* For information on storing and retrieving data you can go to the :doc:`usage documentation </usage>`.
* For information on creating a custom storage backend please see the :doc:`backend API documentation </backends>`.
* If you have found and bug or would like to contribute a feature you can go to the :doc:`contributing guide </contributing>`.