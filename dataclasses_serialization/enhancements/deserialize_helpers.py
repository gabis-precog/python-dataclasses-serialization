import numbers
from datetime import timedelta, datetime
from datetime import timezone
from enum import Enum
from typing import Any, Union
from typing import Optional, Type

from toolz import curry
from typing_inspect import get_args

from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.noop import noop_deserialization
from dataclasses_serialization.serializer_base.typing import dataclass_field_types
from dataclasses_serialization.serializer_base.typing import isinstance


def identity_deserialization_func(key: str) -> str:
    return key


def timedelta_from_milliseconds(value: int) -> timedelta:
    return timedelta(milliseconds=value)


def force_int_deserializer(cls, obj):
    """
    Implicitly converts ints to floats

    Attempt to coerce back
    Fail if coercion lossy
    """

    if isinstance(obj, cls):
        return obj

    try:
        coerced_obj = cls(obj)
    except Exception:
        coerced_obj = None

    if coerced_obj == obj:
        return coerced_obj

    raise DeserializationError("Cannot deserialize {} {!r} to type {}".format(
        type(obj).__name__,
        obj,
        cls.__name__
    ))


def timedelta_deserialize(cls, value: Any) -> timedelta:
    if isinstance(value, timedelta):
        return value

    if isinstance(value, int):
        return timedelta_from_milliseconds(value)

    raise DeserializationError(
        "Cannot deserialize {} to timedelta".format(value)
    )


def number_to_float(cls, value, deserialization_func=noop_deserialization):
    if isinstance(value, float):
        return value

    if not isinstance(value, int):
        raise DeserializationError(
            "Cannot deserialize {} to float".format(value)
        )

    return float(value)


@curry
def dict_to_dataclass(cls,
                      dct,
                      deserialization_func,
                      key_deserialization_func=identity_deserialization_func,
                      serializer=None):
    if not isinstance(dct, dict):
        raise DeserializationError(
            "Cannot deserialize {} {!r} using {}".format(
                type(dct), dct, dict_to_dataclass
            )
        )

    try:
        if serializer is not None:
            fld_types = serializer.get_field_types(cls)
        else:
            fld_types = list(dataclass_field_types(cls, require_bound=True))
    except TypeError:
        raise DeserializationError("Cannot deserialize unbound generic {}".format(cls))

    deserialized_key_dict = {key_deserialization_func(key): value for key, value in dct.items()}

    try:
        init_arguments = {fld.name: deserialization_func(fld_type, deserialized_key_dict[fld.name]) for fld, fld_type in
                          fld_types if fld.name in deserialized_key_dict}
        return cls(**init_arguments)
    except TypeError as exception:
        raise DeserializationError(
            "Missing one or more required fields to deserialize {!r} as {}".format(
                dct, cls
            )
        ) from exception


@curry
def collection_deserialization(type_, obj, target_collection,
                               deserialization_func=noop_deserialization):
    if not isinstance(obj, (list, set, tuple)):
        raise DeserializationError(
            "Cannot deserialize {} {!r} using collection deserialization".format(
                type(obj), obj
            )
        )

    argument_types = get_args(type_, evaluate=True)

    if len(argument_types) == 0:
        return obj

    (value_type, *_) = argument_types

    return target_collection([deserialization_func(value_type, value) for value in obj])


default = object()


def enum_from_name(enum_class: Type[Enum],
                   value: Optional[str],
                   fallback_value: Optional[Enum] = default,
                   value_processor=identity_deserialization_func):
    if value is not None:
        value = value_processor(value)

    for enum in enum_class:
        if enum.name == value:
            return enum

    if fallback_value is not default:
        return fallback_value

    raise Exception('Unknown Enum name "%s" for class "%s"' % (value, enum_class))


def enum_from_value(enum_class: Type[Enum], value: Optional[str]):
    for enum in enum_class:
        if enum.value == value:
            return enum

    raise Exception('Unknown Enum value "%s" for class "%s"' % (value, enum_class))


def datetime_utc_from_timestamp_ms(millis: int) -> datetime:
    return datetime.utcfromtimestamp(millis / 1000)


def datetime_utc_from_inspected_type(data: Union[str, int]) -> datetime:
    if isinstance(data, int):
        return datetime_utc_from_timestamp_ms(data)
    else:
        return datetime_utc_from_formatted(data)


def datetime_utc_from_formatted(date_string: Optional[Union[str, int]], date_format: str = '%Y-%m-%d %H:%M:%S') -> \
        Optional[datetime]:
    if date_string is None:
        return None

    if isinstance(date_string, numbers.Number):
        return datetime_utc_from_timestamp_ms(date_string)

    return datetime.strptime(date_string, date_format).replace(tzinfo=timezone.utc)
