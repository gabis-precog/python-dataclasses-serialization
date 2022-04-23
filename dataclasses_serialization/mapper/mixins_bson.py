from dataclasses_serialization.extensions.bson_helpers import bson_dumps, bson_loads
from dataclasses_serialization.serializer_base import Serializer


def bson_str_serializer_mixin(mapper):
    bson_str_serializer = Serializer(
        serialization_functions={
            object: lambda obj: bson_dumps(mapper.serialize(obj))
        },
        deserialization_functions={
            object: lambda cls, serialized_obj: mapper.deserialize(cls, bson_loads(serialized_obj))
        }
    )

    class Mixin:
        def as_bson_str(self):
            return bson_str_serializer.serialize(self)

        @classmethod
        def from_bson_str(cls, serialized_obj):
            return bson_str_serializer.deserialize(cls, serialized_obj)

    return Mixin


def bson_serializer_mixin(mapper):
    class Mixin:
        def as_bson(self):
            return mapper.serialize(self)

        @classmethod
        def from_bson(cls, serialized_obj):
            return mapper.deserialize(cls, serialized_obj)

    return Mixin
