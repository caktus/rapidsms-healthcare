RapidSMS Healthcare
========================

Welcome to the documentation for rapidsms-healthcare!


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

To test rapidsms-healthcare in mutliple supported environments you can make use
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

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
