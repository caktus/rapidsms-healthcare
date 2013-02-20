RapidSMS Healthcare
========================

rapidsms-healthcare is a reusable Django application for managing healthcare provider
and patient records for building RapidSMS applications. The goal is to create a common
API for storing and accessing these records and have configurable storage backends
for the data itself. For instance on site might store data using a SQL database via
the Django ORM while another might store the data in OpenMRS. Additional Django/RapidSMS
applications can use this API to store and retrive data without knowning how it will be stored.

.. image::
    https://secure.travis-ci.org/caktus/rapidsms-healthcare.png?branch=master
    :alt: Build Status
        :target: https://secure.travis-ci.org/caktus/rapidsms-healthcare


Dependencies
-----------------------------------

rapidsms-appointments currently runs on Python 2.6 and 2.7 and requires the following
Python packages:

- Django >= 1.4
- RapidSMS >= 0.11.0


Documentation
-----------------------------------

Documentation on using rapidsms-healthcare is available on
`Read The Docs <http://readthedocs.org/docs/rapidsms-healthcare/>`_.


Running the Tests
------------------------------------

With all of the dependancies installed, you can quickly run the tests with via::

    python setup.py test

or::

    python runtests.py

To test rapidsms-healthcare in multiple supported environments you can make use
of the `tox <http://tox.readthedocs.org/>`_ configuration.::

    # You must have tox installed
    pip install tox
    # Build default set of environments
    tox
    # Build a single environment
    tox -e py26-1.4.X


License
--------------------------------------

rapidsms-healthcare is released under the BSD License. See the
`LICENSE <https://github.com/caktus/rapidsms-healthcare/blob/master/LICENSE>`_ file for more details.


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out `rapidsms-healthcare on Github <https://github.com/caktus/rapidsms-healthcare>`_.
A full contributing guide can be found in the
`online documentation <http://rapidsms-healthcare.readthedocs.org/en/latest/contributing.html>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
