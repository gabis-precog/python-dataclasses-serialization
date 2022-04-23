import json
from typing import Union, Optional, Type, Any, TypeVar

from toolz import identity, curry

from dataclasses_serialization.mapper.defaults import build_init_arguments, default_serializers, default_deserializers
from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.mapper.mapper import Mapper
from dataclasses_serialization.mapper.typing import SerializerMap

__all__ = [
    'JsonMapper'
]

T = TypeVar('T')


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

    @curry
    def from_json(self, cls: Type[T], data: Union[str, bytes], **kwargs) -> Optional[T]:
        return self.deserialize(cls, json.loads(data, **kwargs))

    def to_json(self, data: Any, **kwargs) -> str:
        return json.dumps(self.serialize(data), **kwargs)
