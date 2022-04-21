from typing import Optional

import bson

from dataclasses_serialization.bson import bson_int_deserializer
from dataclasses_serialization.enhancements.argument_helpers import merge_lazy_dicts
from dataclasses_serialization.enhancements.mapper import Serializer
from dataclasses_serialization.enhancements.typing import SerializerMap
from dataclasses_serialization.serializer_base import noop_deserialization, noop_serialization
from dataclasses_serialization.serializer_base.noop import identity


class BsonMapper(Serializer):
    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = None,
                 deserialization_functions: Optional[SerializerMap] = None,
                 key_serializer=identity,
                 key_deserializer=identity):
        super().__init__(
            serialization_functions=merge_lazy_dicts(self, serialization_functions, {
                bson.ObjectId: noop_serialization
            }),
            deserialization_functions=merge_lazy_dicts(self, deserialization_functions, {
                int: bson_int_deserializer,
                bson.ObjectId: noop_deserialization
            }),
            key_serializer=key_serializer,
            key_deserializer=key_deserializer
        )
