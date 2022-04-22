from typing import Optional

from dataclasses_serialization.mapper.defaults import build_init_arguments
from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.mapper.mapper import Mapper
from dataclasses_serialization.mapper.typing import SerializerMap
from dataclasses_serialization.serializer_base.noop import identity

__all__ = [
    'JsonMapper'
]

_default = object()


class JsonMapper(Mapper):
    """
    Mapper with sane defaults for json de/serializing.

    Example usage:

    >>> mapper = JsonMapper()
    >>> mapper.serialize([1,2,3])
    [1, 2, 3]
    """

    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = _default,
                 deserialization_functions: Optional[SerializerMap] = _default,
                 key_serializer=identity,
                 key_deserializer=identity
                 ):
        super().__init__(**build_init_arguments(serialization_functions,
                                                deserialization_functions,
                                                key_serializer,
                                                key_deserializer,
                                                _default))

        self.register_deserializer(int, force_int_deserializer)
