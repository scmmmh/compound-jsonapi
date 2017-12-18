Offline JSONAPI
===============

The Offline JSONAPI package is an extension to `Marshmallow`_ and has been
heavily influenced by `Marshmallow JSONAPI`_. The difference to
`Marshmallow JSONAPI`_ is that the Offline JSONAPI is focused on loading
and dumping objects to compound JSONAPI documents that contain all the
serialised data, rather than using JSONAPI's link functionality. It has one
main advantage over `Marshmallow JSONAPI`_ in that it can load and dump full
circular graph structures.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`Marshmallow`: http://marshmallow.readthedocs.io
.. _`Marshmallow JSONAPI`: http://marshmallow-jsonapi.readthedocs.io
