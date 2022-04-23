"""

Extensions are available to handle some non-native data types:
 - dateutil
 - key_mapping
 - numpy

Install using the pip extensions mechanism.

>>> from dataclasses_serialization.mapper.json_mapper import JsonMapper

Dateutil
--------

Support for mapping relativedelta fields to and from milliseconds. Example usage:

>>> from dataclasses_serialization.extensions.dateutil_helpers import (dateutil_serializers,
...                                                                    dateutil_deserializers)
>>> from dateutil.relativedelta import relativedelta

>>> mapper = (JsonMapper()
...                     .register_serializers(dateutil_serializers)
...                     .register_deserializers(dateutil_deserializers)
...                 )
>>> mapper.serialize(relativedelta(days=4, minutes=5))
345900000

>>> mapper.deserialize(relativedelta, 345900000)
relativedelta(days=+4, minutes=+5)

Numpy
-----

Support for mapping some numpy types. Example usage:

>>> from dataclasses_serialization.extensions.numpy_helpers import (numpy_serializers,
...                                                                 numpy_deserializers)
>>> import numpy

>>> mapper = (JsonMapper()
...                     .register_serializers(numpy_serializers)
...                     .register_deserializers(numpy_deserializers)
...                 )
>>> mapper.serialize(numpy.array([[1,2,3],[4,5,6]]))
[[1, 2, 3], [4, 5, 6]]

>>> mapper.deserialize(numpy.ndarray, [[1,2,3],[4,5,6]])
array([[1, 2, 3],
       [4, 5, 6]])
"""
