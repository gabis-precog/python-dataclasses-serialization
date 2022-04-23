import numbers
from datetime import timedelta, datetime
from datetime import timezone
from typing import Any, Union
from typing import Optional

from toolz import curry
from typing_inspect import get_args

from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.noop import noop_deserialization
from dataclasses_serialization.serializer_base.typing import dataclass_field_types
from dataclasses_serialization.serializer_base.typing import is_instance


def identity_deserialization_func(key: str) -> str:
    return key


def timedelta_from_milliseconds(value: int) -> timedelta:
    return timedelta(milliseconds=value)


def force_int_deserializer(cls, obj):
    """
    Explicitly converts ints to floats

    Attempt to coerce back
    Fail if coercion lossy
    """

    if is_instance(obj, cls):
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


def number_to_float(cls, value) -> float:
    """
    Force serializing numbers as floats.
    """
    if is_instance(value, float):
        return value

    try:
        return float(value)
    except Exception:
        raise DeserializationError(
            "Cannot deserialize {} to float".format(value)
        )


@curry
def dict_to_dataclass(cls,
                      dct,
                      deserialization_func,
                      key_deserialization_func=identity_deserialization_func,
                      serializer=None):
    if not is_instance(dct, dict):
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
        init_arguments = {}
        for fld, fld_type in fld_types:
            if fld.name in deserialized_key_dict:
                init_arguments[fld.name] = deserialization_func(fld_type, deserialized_key_dict[fld.name])

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
    if not is_instance(obj, (list, set, tuple)):
        raise DeserializationError(
            "Cannot deserialize {} {!r} using collection deserialization".format(
                type(obj), obj
            )
        )

    argument_types = get_args(type_, evaluate=True)

    if len(argument_types) == 0:
        return target_collection(obj)

    value_type = argument_types[0]

    return target_collection([deserialization_func(value_type, value) for value in obj])


def datetime_utc_from_timestamp_ms(millis: int) -> datetime:
    return datetime.utcfromtimestamp(millis / 1000)


def datetime_utc_from_inspected_type(data: Union[str, int]) -> datetime:
    if is_instance(data, int):
        return datetime_utc_from_timestamp_ms(data)
    else:
        return datetime_utc_from_formatted(data)


def datetime_utc_from_formatted(date_string: Optional[Union[str, int]], date_format: str = '%Y-%m-%d %H:%M:%S') -> \
        Optional[datetime]:
    if date_string is None:
        return None

    if is_instance(date_string, numbers.Number):
        return datetime_utc_from_timestamp_ms(date_string)

    return datetime.strptime(date_string, date_format).replace(tzinfo=timezone.utc)
