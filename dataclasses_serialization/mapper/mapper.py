import json
from typing import Union, Optional, TypeVar, Type, Any

from toolz import curry

from dataclasses_serialization.mapper.argument_helpers import merge_lazy_dicts
from dataclasses_serialization.mapper.typing import SerializerMap
from dataclasses_serialization.serializer_base import Serializer as BaseSerialize
from dataclasses_serialization.serializer_base.noop import identity
from dataclasses_serialization.serializer_base.typing import dataclass_field_types

__all__ = ['Mapper']

T = TypeVar('T')


class Mapper(BaseSerialize):
    """
    Base mapper class without any specific serializers/deserializers registered.

    Unless you want to customize things from scratch, use one of the subclasses (eg. JsonMapper).
    """

    def __init__(self,
                 serialization_functions: SerializerMap = None,
                 deserialization_functions: SerializerMap = None,
                 key_serializer=identity,
                 key_deserializer=identity
                 ):
        self._key_serializer = key_serializer
        self._key_deserializer = key_deserializer

        super().__init__(
            merge_lazy_dicts(self, serialization_functions),
            merge_lazy_dicts(self, deserialization_functions)
        )

        self.field_types_cache = {}

    def get_field_types(self, cls):
        fld_types = self.field_types_cache.get(cls)

        if fld_types is None:
            fld_types = list(dataclass_field_types(cls, require_bound=True))
            self.field_types_cache[cls] = fld_types
        return fld_types

    @curry
    def deserialize(self, cls: Type[T], serialized_obj) -> Optional[T]:
        if serialized_obj is None:
            return None

        return super().deserialize(cls, serialized_obj)

    @curry
    def from_json(self, cls: Type[T], data: Union[str, bytes], **kwargs) -> Optional[T]:
        return self.deserialize(cls, json.loads(data, **kwargs))

    def to_json(self, data: Any, **kwargs) -> str:
        return json.dumps(self.serialize(data), **kwargs)

    def register_serializers(self, serializers: SerializerMap):
        """

        Register multiple serializers. Adds or overrides existing.

        >>> from dataclasses_serialization.serializer_base import noop_serialization
        >>> mapper = Mapper().register_serializers({int:noop_serialization})

        """
        if callable(serializers):
            serializers = serializers(self)

        for key, value in serializers.items():
            if isinstance(key, tuple):
                for sub_key in key:
                    self.register_serializer(sub_key, value)
            else:
                self.register_serializer(key, value)

        return self

    def register_deserializers(self, deserializers: SerializerMap):
        """

        Register multiple deserializers. Adds or overrides existing.

        >>> from dataclasses_serialization.mapper.deserialize_helpers import force_int_deserializer
        >>> mapper = Mapper().register_deserializers({int:force_int_deserializer})

        """
        if callable(deserializers):
            deserializers = deserializers(self)

        for key, value in deserializers.items():
            if isinstance(key, tuple):
                for sub_key in key:
                    self.register_deserializer(sub_key, value)
            else:
                self.register_deserializer(key, value)

        return self
