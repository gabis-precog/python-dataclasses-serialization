from dataclasses_serialization.enhancements.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.enhancements.mapper import Serializer
from dataclasses_serialization.serializer_base import noop_serialization


class JsonMapper(Serializer):
    def __init__(self, key_serializer=noop_serialization):
        super().__init__(
            deserialization_functions=lambda default_serializer: {
                int: force_int_deserializer
            },
            key_serializer=key_serializer)
