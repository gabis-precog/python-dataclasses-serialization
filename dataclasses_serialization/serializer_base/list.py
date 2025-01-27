from typing import List

from toolz import curry
from typing_inspect import get_args

from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.noop import noop_deserialization
from dataclasses_serialization.serializer_base.typing import is_instance

__all__ = ["list_deserialization"]


@curry
def list_deserialization(type_, obj, deserialization_func=noop_deserialization):
    if not is_instance(obj, list):
        raise DeserializationError(
            "Cannot deserialize {} {!r} using list deserialization".format(
                type(obj), obj
            )
        )

    if type_ is list or type_ is List:
        return obj

    (value_type,) = get_args(type_, evaluate=True)

    return [deserialization_func(value_type, value) for value in obj]
