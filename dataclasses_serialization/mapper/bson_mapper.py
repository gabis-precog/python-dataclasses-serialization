from typing import Optional

import bson
from toolz import identity

from dataclasses_serialization.mapper.defaults import build_init_arguments, default_deserializers, default_serializers
from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.mapper.mapper import Mapper
from dataclasses_serialization.mapper.typing import SerializerMap
from dataclasses_serialization.serializer_base import noop_deserialization, noop_serialization

__all__ = ['BsonMapper']


class BsonMapper(Mapper):
    """
    Mapper with sane defaults for bson de/serializing.

    Example usage:

    >>> mapper = BsonMapper()
    >>> mapper.serialize([1,2,3])
    [1, 2, 3]
    """

    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = default_serializers,
                 deserialization_functions: Optional[SerializerMap] = default_deserializers,
                 key_serializer=identity,
                 key_deserializer=identity):
        super().__init__(**build_init_arguments(serialization_functions,
                                                deserialization_functions,
                                                key_serializer,
                                                key_deserializer))

        self.register_serializer(bson.ObjectId, noop_serialization)
        self.register_deserializer(bson.ObjectId, noop_deserialization)
        self.register_deserializer(int, force_int_deserializer)
