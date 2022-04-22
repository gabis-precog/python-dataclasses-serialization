"""
Helpers for serializing/deserializing enums. Not included in the defaults since it should be defined explicitly by the user.
"""


from enum import Enum
from typing import Optional, Type, Any

from dataclasses_serialization.mapper.deserialize_helpers import identity_deserialization_func

default = object()


def enum_from_name(enum_class: Type[Enum],
                   value: Optional[str],
                   fallback_value: Optional[Enum] = default,
                   value_processor=identity_deserialization_func):
    """
    Deserialize enum from it's name.
    """
    if value is not None:
        value = value_processor(value)

    for enum in enum_class:
        if enum.name == value:
            return enum

    if fallback_value is not default:
        return fallback_value

    raise Exception('Unknown Enum name "%s" for class "%s"' % (value, enum_class))


def enum_from_value(enum_class: Type[Enum], value: Optional[str]):
    """
    Deserialize enum from it's value.
    """
    for enum in enum_class:
        if enum.value == value:
            return enum

    raise Exception('Unknown Enum value "%s" for class "%s"' % (value, enum_class))


def enum_to_name(item) -> str:
    """
    Serialize enum using it's name.
    """
    return item.name


def enum_to_value(item) -> Any:
    """
    Serialize enum using it's value.
    """
    return item.value
