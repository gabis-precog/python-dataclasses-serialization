from typing import Optional

from dataclasses_serialization.mapper.defaults import build_init_arguments, default_serializers, default_deserializers
from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.mapper.mapper import Mapper
from dataclasses_serialization.mapper.typing import SerializerMap
from dataclasses_serialization.serializer_base.noop import identity

__all__ = [
    'JsonMapper'
]


class JsonMapper(Mapper):
    """
    Mapper with sane defaults for json de/serializing.

    Example usage:

    >>> mapper = JsonMapper()
    >>> mapper.serialize([1,2,3])
    [1, 2, 3]
    """

    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = default_serializers,
                 deserialization_functions: Optional[SerializerMap] = default_deserializers,
                 key_serializer=identity,
                 key_deserializer=identity
                 ):
        super().__init__(**build_init_arguments(serialization_functions,
                                                deserialization_functions,
                                                key_serializer,
                                                key_deserializer))

        self.register_deserializer(int, force_int_deserializer)
