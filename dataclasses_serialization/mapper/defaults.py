"""
Customize mapping
=================

To create a custom mapper, create an instance of `dataclasses_serialization.mapper.json_mapper.JsonMapper`.
The mapping can be either overridden, or expand on the defaults.

>>> from dataclasses_serialization.mapper.mapper import Mapper
>>> from dataclasses_serialization.mapper.json_mapper import JsonMapper
>>> from dataclasses_serialization.serializer_base import (
...             noop_serialization, noop_deserialization, dict_serialization,
...             dict_deserialization, list_deserialization
...           )

To override the defaults completely, pass new values to **serialization_functions** and **deserialization_functions** arguments.
To leave the defaults, instantiate a JsonMapper, and supply `dataclasses_serialization.mapper.mapper.Mapper.register_serializers`
and `dataclasses_serialization.mapper.mapper.Mapper.register_deserializers` with the new mapping methods:

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

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from pathlib import PurePath

from dataclasses_serialization.mapper.deserialize_helpers import timedelta_deserialize, dict_to_dataclass, \
    collection_deserialization, number_to_float, datetime_utc_from_inspected_type
from dataclasses_serialization.mapper.serializer_helpers import keep_not_none_value, timedelta_to_milliseconds, \
    datetime_to_milliseconds, float_serializer
from dataclasses_serialization.serializer_base import noop_serialization, \
    dict_serialization, noop_deserialization, dict_deserialization

__all__ = [
    'default_serializers',
    'default_deserializers'
]


def default_serializers(mapper) -> dict:
    return {
        dataclass: lambda value: mapper.serialize(
            keep_not_none_value(dict_serialization(value.__dict__, key_serialization_func=mapper._key_serializer))),
        dict: lambda dct: keep_not_none_value(dict_serialization(
            dct,
            key_serialization_func=mapper.serialize,
            value_serialization_func=mapper.serialize)),
        datetime: datetime_to_milliseconds,
        (tuple, set, list, frozenset): lambda lst: list(map(mapper.serialize, lst)),
        str: noop_serialization,
        int: noop_serialization,
        float: float_serializer,
        bool: noop_serialization,
        timedelta: timedelta_to_milliseconds,
        PurePath: lambda value: str(value),
        type(None): noop_serialization,
    }


def default_deserializers(mapper) -> dict:
    return {
        timedelta: timedelta_deserialize,
        datetime: lambda cls, value: datetime_utc_from_inspected_type(value),
        dataclass: lambda cls, value: dict_to_dataclass(cls, value, mapper.deserialize, mapper._key_deserializer,
                                                        serializer=mapper),
        dict: dict_deserialization(key_deserialization_func=mapper.deserialize,
                                   value_deserialization_func=mapper.deserialize),
        list: collection_deserialization(target_collection=list,
                                         deserialization_func=mapper.deserialize),
        set: collection_deserialization(target_collection=set,
                                        deserialization_func=mapper.deserialize),
        frozenset: collection_deserialization(target_collection=frozenset,
                                              deserialization_func=mapper.deserialize),
        tuple: collection_deserialization(target_collection=tuple,
                                          deserialization_func=mapper.deserialize),
        str: noop_deserialization,
        float: number_to_float,
        bool: noop_deserialization,
        Path: lambda cls, value: Path(value),
        type(None): noop_deserialization
    }


def build_init_arguments(serialization_functions,
                         deserialization_functions,
                         key_serializer,
                         key_deserializer,
                         default_marker):
    init_kwargs = dict(
        key_serializer=key_serializer,
        key_deserializer=key_deserializer
    )

    if serialization_functions is not default_marker:
        init_kwargs['serialization_functions'] = serialization_functions

    if deserialization_functions is not default_marker:
        init_kwargs['deserialization_functions'] = deserialization_functions

    return init_kwargs
