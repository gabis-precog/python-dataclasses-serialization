import bson

from dataclasses_serialization.bson import bson_int_deserializer
from dataclasses_serialization.enhancements.mapper import Serializer
from dataclasses_serialization.serializer_base import noop_deserialization


class BsonMapper(Serializer):
    def __init__(self):
        super().__init__(
            serialization_functions=lambda default_serializer: {
                bson.ObjectId: noop_deserialization,

            },
            deserialization_functions=lambda default_serializer: {

                int: bson_int_deserializer,
                bson.ObjectId: noop_deserialization,
            })
