from typing import Optional, Union, Callable

from dataclasses_serialization.enhancements.deserialize_helpers import force_int_deserializer
from dataclasses_serialization.enhancements.mapper import Serializer
from dataclasses_serialization.serializer_base import noop_serialization


class JsonMapper(Serializer):
    def __init__(self,
                 serialization_functions: Optional[Union[dict, Callable[[Serializer], dict]]] = None,
                 deserialization_functions: Optional[Union[dict, Callable[[Serializer], dict]]] = None,
                 key_serializer=noop_serialization,
                 ):
        super().__init__(
            serialization_functions=serialization_functions,
            deserialization_functions=deserialization_functions or {
                int: force_int_deserializer
            },
            key_serializer=key_serializer)
