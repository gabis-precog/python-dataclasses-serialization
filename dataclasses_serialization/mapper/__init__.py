"""

To create a custom mapper, create an instance of `dataclasses_serialization.mapper.json_mapper.JsonMapper`.
The mapping can be either overridden, or expand on the defaults.

>>> from dataclasses_serialization.mapper.mapper import Mapper
>>> from dataclasses_serialization.mapper.json_mapper import JsonMapper
>>> from dataclasses_serialization.serializer_base import (
...             noop_serialization, noop_deserialization, dict_serialization,
...             dict_deserialization, list_deserialization
...           )

To override the defaults completely, pass new values to **serialization_functions** and **deserialization_functions**
arguments.

>>> custom_mapper = Mapper(
...    serialization_functions=lambda mapper: {
...        list: (lambda lst: list(map(mapper.serialize, lst))),
...        (str, int, float, bool, type(None)): noop_serialization
...    },
...    deserialization_functions=lambda mapper: {
...        list: (lambda cls, lst: list_deserialization(cls, lst, deserialization_func=mapper.deserialize)),
...        (str, int, float, bool, type(None)): noop_deserialization
...    }
...  )

To add or override the existing defaults use the **register** methods:

**register_deserializers**:

>>> from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
>>> mapper = Mapper().register_deserializers({int:force_int_deserializer})
>>> mapper.deserialize(int, 5.0)
5

**register_serializers**:

>>> from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
>>> mapper = Mapper().register_serializers({int:float})
>>> mapper.serialize(5)
5.0
"""
