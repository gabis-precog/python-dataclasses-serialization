import json

from dataclasses_serialization.serializer_base import Serializer


def json_str_serializer_mixin(mapper):
    json_str_serializer = Serializer(
        serialization_functions={
            object: lambda obj: json.dumps(mapper.serialize(obj))
        },
        deserialization_functions={
            object: lambda cls, serialized_obj: mapper.deserialize(cls, json.loads(serialized_obj))
        }
    )

    class Mixin:
        def as_json_str(self):
            return json_str_serializer.serialize(self)

        @classmethod
        def from_json_str(cls, serialized_obj):
            return json_str_serializer.deserialize(cls, serialized_obj)

    return Mixin


def json_serializer_mixin(mapper):
    class Mixin:
        def as_json(self):
            return mapper.serialize(self)

        @classmethod
        def from_json(cls, serialized_obj):
            return mapper.deserialize(cls, serialized_obj)

    return Mixin
