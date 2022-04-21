from typing import Optional

import bson

from dataclasses_serialization.bson import bson_int_deserializer
from dataclasses_serialization.mapper.mapper import Mapper
from dataclasses_serialization.mapper.typing import SerializerMap
from dataclasses_serialization.serializer_base import noop_deserialization, noop_serialization
from dataclasses_serialization.serializer_base.noop import identity

_default = object()

__all__ = ['BsonMapper']


class BsonMapper(Mapper):
    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = _default,
                 deserialization_functions: Optional[SerializerMap] = _default,
                 key_serializer=identity,
                 key_deserializer=identity):

        init_kwargs = dict(
            key_serializer=key_serializer,
            key_deserializer=key_deserializer
        )

        if serialization_functions is not _default:
            init_kwargs['serialization_functions'] = serialization_functions

        if deserialization_functions is not _default:
            init_kwargs['deserialization_functions'] = deserialization_functions,

        super().__init__(**init_kwargs)

        self.register_serializer(bson.ObjectId, noop_serialization)
        self.register_deserializer(bson.ObjectId, noop_deserialization)
        self.register_deserializer(int, bson_int_deserializer)
