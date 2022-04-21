from typing import Optional

from dataclasses_serialization.enhancements.argument_helpers import merge_lazy_dicts
from dataclasses_serialization.enhancements.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.enhancements.mapper import Serializer
from dataclasses_serialization.enhancements.typing import SerializerMap
from dataclasses_serialization.serializer_base import noop_serialization


class JsonMapper(Serializer):
    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = None,
                 deserialization_functions: Optional[SerializerMap] = None,
                 key_serializer=noop_serialization,
                 ):
        super().__init__(
            serialization_functions=serialization_functions,
            deserialization_functions=merge_lazy_dicts(self, deserialization_functions, {
                int: force_int_deserializer
            }),
            key_serializer=key_serializer)
