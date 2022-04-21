from toolz import curry

from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.typing import is_instance

__all__ = ["noop_serialization", "noop_deserialization"]


def noop_serialization(obj):
    return obj


@curry
def noop_deserialization(cls, obj):
    if not is_instance(obj, cls):
        raise DeserializationError(
            "Cannot deserialize {} {!r} to type {}".format(type(obj), obj, cls)
        )

    return obj
