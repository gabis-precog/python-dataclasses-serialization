"""
Extensions
==========

Extensions are available to handle some non-native data types:
- dateutil
- key_mapping
- numpy

Install using the pip extensions mechanism.

Dateutil
--------

Support for mapping relativedelta fields to and from milliseconds. Example usage:
>>> from dataclasses_serialization.mapper.json_mapper import JsonMapper
>>> from dataclasses_serialization.extensions.dateutil_helpers import (dateutil_serializers,
...                                                                    dateutil_deserializers)
>>> from dateutil.relativedelta import relativedelta

>>> mapper = (JsonMapper()
...                     .register_serializers(dateutil_serializers)
...                     .register_deserializers(dateutil_deserializers)
...                 )
>>> mapper.serialize(relativedelta(days=4, minutes=5))
345900000
"""
