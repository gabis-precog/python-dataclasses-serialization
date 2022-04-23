"""

Extensions are available to handle some non-native data types:
 - dateutil
 - key_mapping
 - numpy
 - attrs

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

attrs
-----

Support for mapping attrs classes which have type hints.


>>> from dataclasses_serialization.extensions.attrs_helpers import attrs_serializers, attrs_deserializers
>>> from dataclasses_serialization.mapper.json_mapper import JsonMapper

Assumeing an attrs supported class is defined:

>>> from typing import Dict
>>> from attr import define
>>> @define
... class SampleAttrs:
...    number: int
...    name: str
...    lookup: Dict[str, int]

Define a mapper with attrs support:

>>> mapper = (JsonMapper()
...           .register_serializers(attrs_serializers)
...           .register_deserializers(attrs_deserializers)
...          )

An instance can be serialized:

>>> item = SampleAttrs(3, 'a', {'b': 2})
>>> mapper.serialize(item)
{'number': 3, 'name': 'a', 'lookup': {'b': 2}}

And deserialized:

>>> item = {'number': 3, 'name': 'a', 'lookup': {'b': 2}}
>>> mapper.deserialize(SampleAttrs, item)
SampleAttrs(number=3, name='a', lookup={'b': 2})

"""

