elife-tools
===========

Tools for using article data in Python

Supports
============

* Python >=3.5

Non-Python dependencies
=======================

* libxml2 (Ubuntu, Arch)

Install for users
=================

Install via `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: bash

   $ pip install elifetools
   
You might need to install libxml manually first

.. code-block:: bash

   $ sudo STATIC_DEPS=true pip install lxml==3.4.1

To install the latest version directly from git

.. code-block:: bash

   $ pip install git+https://github.com/elifesciences/elife-tools.git@master

or you can add it to your project's requirements.txt file

.. code-block:: bash

   git+https://github.com/elifesciences/elife-tools.git@master


Install for developers
======================

Clone the git repo

Make a virtualenv (optional)

Then

.. code-block:: bash

   $ python setup.py install

Example usage
=============

.. code-block:: python

    >>> from elifetools import parseJATS as parser
    >>> soup = parser.parse_document('tests/sample-xml/elife-kitchen-sink.xml')
    >>> print(parser.doi(soup))

More code examples can be found in `tests/basic_usage_test.py`


Testing
=======

You can run the full automated test suite from the base folder with:

.. code-block:: bash

    $ python -m unittest discover tests

or you can run tests with coverage:

.. code-block:: bash

    $ coverage run -m unittest discover tests

and then view the coverage report:

.. code-block:: bash

    $ coverage report -m


License
=========

`The MIT License <http://opensource.org/licenses/mit-license.php>`_
