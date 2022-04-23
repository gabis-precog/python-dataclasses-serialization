from typing import Optional

from pydash import camel_case

from dataclasses_serialization.mapper.defaults import build_init_arguments
from dataclasses_serialization.mapper.json_mapper import JsonMapper
from dataclasses_serialization.mapper.typing import SerializerMap
from toolz import identity

_default = object()


class JavaJsonMapper(JsonMapper):
    def __init__(self,
                 serialization_functions: Optional[SerializerMap] = _default,
                 deserialization_functions: Optional[SerializerMap] = _default,
                 key_serializer=camel_case,
                 key_deserializer=identity):
        super().__init__(**build_init_arguments(serialization_functions,
                                                deserialization_functions,
                                                key_serializer,
                                                key_deserializer,
                                                _default))
