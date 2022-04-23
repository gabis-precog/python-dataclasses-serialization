.. Dataclasses Serialization documentation master file, created by
   sphinx-quickstart on Fri Apr 22 11:01:09 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dataclasses Serialization
=========================

.. toctree::
   :maxdepth: 1

   quickstart
   customize
   extensions
   api
   changelog

.. autosummary::
   :toctree: generated


`dataclasses_serialization` provides serializers/deserializers for transforming between Python dataclasses,
and JSON and BSON objects. Support is available for:
* dataclasses
* attrs classes
* python native types (including Enums)
* relativedelta (dateutil)
* numpy (int64, bool, ndarray)
* key normalization for python (underscore) and java (camelCase) conventions
* bson

.. note::
   This documentation is for the fork at https://github.com/gabis-precog/python-dataclasses-serialization.
   This project is (or aims to be) backwards compatible with the original project, So some documentation
   here may apply to (and is based on the documentation of) the original.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
