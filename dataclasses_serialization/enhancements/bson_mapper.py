from typing import Optional, Union, Callable

import bson

from dataclasses_serialization.bson import bson_int_deserializer
from dataclasses_serialization.enhancements.argument_helpers import merge_lazy_dicts
from dataclasses_serialization.enhancements.mapper import Serializer
from dataclasses_serialization.serializer_base import noop_deserialization, noop_serialization


class BsonMapper(Serializer):
    def __init__(self,
                 serialization_functions: Optional[Union[dict, Callable[[Serializer], dict]]] = None,
                 deserialization_functions: Optional[Union[dict, Callable[[Serializer], dict]]] = None, ):
        super().__init__(
            serialization_functions=merge_lazy_dicts(self, serialization_functions, {
                bson.ObjectId: noop_serialization
            }),
            deserialization_functions=merge_lazy_dicts(self, deserialization_functions, {
                int: bson_int_deserializer,
                bson.ObjectId: noop_deserialization
            })
        )
