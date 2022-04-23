"""
Default set of serializer/deserializers for python primitives (dataclass, collections, numeric primitives etc.)

These are the defaults used in JsonMapper and BsonMapper.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from pathlib import PurePath

from toolz import curry

from dataclasses_serialization.mapper.deserialize_helpers import timedelta_deserialize, dict_to_dataclass, \
    collection_deserialization, number_to_float, datetime_utc_from_inspected_type
from dataclasses_serialization.mapper.serialize_helpers import keep_not_none_value, timedelta_to_milliseconds, \
    datetime_to_milliseconds, float_serializer
from dataclasses_serialization.serializer_base import noop_serialization, \
    dict_serialization, noop_deserialization, dict_deserialization

__all__ = [
    'default_serializers',
    'default_deserializers'
]


@curry
def default_serializers(mapper, dict_post_processor=keep_not_none_value) -> dict:
    """
    Set of default serializers useful as a base for json/bson
    """
    return {
        dataclass: lambda value: dict_serialization(value.__dict__,
                                                    key_serialization_func=mapper._key_serializer,
                                                    value_serialization_func=mapper.serialize,
                                                    post_processor=dict_post_processor),
        dict: dict_serialization(
            key_serialization_func=mapper.serialize,
            value_serialization_func=mapper.serialize,
            post_processor=dict_post_processor),
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
    """
    Set of default deserializers useful as a base for json/bson
    """
    return {
        timedelta: timedelta_deserialize,
        datetime: datetime_utc_from_inspected_type,
        dataclass: dict_to_dataclass(deserialization_func=mapper.deserialize,
                                     key_deserialization_func=mapper._key_deserializer,
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
                         default_marker=None):
    init_kwargs = dict(
        key_serializer=key_serializer,
        key_deserializer=key_deserializer
    )

    if serialization_functions is not default_marker:
        init_kwargs['serialization_functions'] = serialization_functions

    if deserialization_functions is not default_marker:
        init_kwargs['deserialization_functions'] = deserialization_functions

    return init_kwargs
