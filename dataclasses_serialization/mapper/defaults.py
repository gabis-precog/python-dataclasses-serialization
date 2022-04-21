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


def default_serializers(mapper):
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


def default_deserializers(mapper):
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
