import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from math import isnan, isinf
from pathlib import Path
from pathlib import PurePath
from typing import Callable, Union, Optional, TypeVar, Type, Any

from pathlib2 import PurePath as PurePath2, Path as Path2
from toolz import curry

from dataclasses_serialization.enhancements.deserialize_helpers import timedelta_deserialize, dict_to_dataclass, \
    collection_deserialization, number_to_float, datetime_utc_from_inspected_type
from dataclasses_serialization.enhancements.key_helpers import normalize_key_case
from dataclasses_serialization.enhancements.serializer_helpers import keep_not_none_value, timedelta_to_milliseconds, \
    datetime_to_milliseconds
from dataclasses_serialization.serializer_base import Serializer as BaseSerialize, noop_serialization, \
    dict_serialization, noop_deserialization, dict_deserialization
from dataclasses_serialization.serializer_base.typing import dataclass_field_types

__all__ = ['Serializer']

T = TypeVar('T')


class Serializer(BaseSerialize):
    def __init__(self,
                 serialization_functions: Optional[Union[dict, Callable]] = None,
                 deserialization_functions: Optional[Union[dict, Callable]] = None,
                 key_serializer=noop_serialization
                 ):
        self._key_serializer = key_serializer
        serialization_functions = serialization_functions or {}
        deserialization_functions = deserialization_functions or {}

        if callable(serialization_functions):
            serialization_functions = serialization_functions(self)

        if callable(deserialization_functions):
            deserialization_functions = deserialization_functions(self)

        super().__init__({**self._shared_serializers(), **serialization_functions},
                         {**self._shared_deserializers(), **deserialization_functions})

        self.field_types_cache = {}

        self.serialization_functions.setdefault(
            Enum, lambda value: value.value
        )

    def _shared_serializers(self):
        return {
            dataclass: lambda value: self.serialize(
                keep_not_none_value(dict_serialization(value.__dict__, key_serialization_func=self._key_serializer))),
            dict: lambda dct: keep_not_none_value(dict_serialization(
                dct,
                key_serialization_func=self.serialize,
                value_serialization_func=self.serialize)),
            # (EntityType, FieldActivityType, HintActionTypes, HintFeedbackTypes,
            #  MessageTaskType, AlgorithmType, ChangeOperationType,
            #  MLModelDirtyState, CentralityOrientation, CentralityFunction): lambda value: value.name,
            # (ConditionOperator, ConditionReduceOperator, AbstractFailReasonEnum): lambda value: value.value,
            datetime: datetime_to_milliseconds,
            (tuple, set, list, frozenset): lambda lst: list(map(self.serialize, lst)),
            str: noop_serialization,
            int: noop_serialization,
            float: self._float_serializer,
            bool: noop_serialization,
            timedelta: timedelta_to_milliseconds,
            (PurePath, PurePath2): lambda value: str(value),
            type(None): noop_serialization,
        }

    def _float_serializer(self, value: float) -> Optional[float]:
        if isinstance(value, float):
            if isnan(value):
                return None
            if isinf(value):
                return None  # todo: is this a good idea ?
        return value

    def _shared_deserializers(self):
        return {

            timedelta: timedelta_deserialize,
            datetime: lambda cls, value: datetime_utc_from_inspected_type(value),
            dataclass: lambda cls, value: dict_to_dataclass(cls, value, self.deserialize, normalize_key_case,
                                                            serializer=self),
            dict: dict_deserialization(key_deserialization_func=self.deserialize,
                                       value_deserialization_func=self.deserialize),
            # Dict: dict_deserialization(key_deserialization_func=self.deserialize,
            #                            value_deserialization_func=self.deserialize),
            list: collection_deserialization(target_collection=list,
                                             deserialization_func=self.deserialize),
            # List: collection_deserialization(target_collection=list,
            #                                  deserialization_func=self.deserialize),
            set: collection_deserialization(target_collection=set,
                                            deserialization_func=self.deserialize),
            # Set: collection_deserialization(target_collection=set,
            #                                 deserialization_func=self.deserialize),
            # FrozenSet: collection_deserialization(target_collection=frozenset,
            #                                       deserialization_func=self.deserialize),
            frozenset: collection_deserialization(target_collection=frozenset,
                                                  deserialization_func=self.deserialize),
            tuple: collection_deserialization(target_collection=tuple,
                                              deserialization_func=self.deserialize),
            # Tuple: collection_deserialization(target_collection=tuple,
            #                                   deserialization_func=self.deserialize),
            str: noop_deserialization,
            float: number_to_float,
            bool: noop_deserialization,
            Path2: lambda cls, value: Path2(value),
            Path: lambda cls, value: Path(value),
            type(None): noop_deserialization
        }

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
    def from_json(self, cls: Type[T], data: Union[str, bytes]) -> Optional[T]:
        return self.deserialize(cls, json.loads(data))

    def to_json(self, data: Any) -> str:
        return json.dumps(self.serialize(data))
