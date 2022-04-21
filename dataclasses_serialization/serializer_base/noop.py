from toolz import curry

from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.typing import is_instance

__all__ = [
    "identity",
    "noop_serialization",
    "noop_deserialization"
]


def identity(value):
    return value


def noop_serialization(obj):
    return obj


@curry
def noop_deserialization(cls, obj):
    if not is_instance(obj, cls):
        raise DeserializationError(
            "Cannot deserialize {} {!r} to type {}".format(type(obj), obj, cls)
        )

    return obj
