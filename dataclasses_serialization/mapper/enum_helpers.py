"""
Helpers for serializing/deserializing enums. Not included in the defaults since it should be defined explicitly by the user.
"""

from enum import Enum
from typing import Optional, Type, Any

from toolz import curry

from dataclasses_serialization.mapper.deserialize_helpers import identity_deserialization_func

default = object()


@curry
def enum_from_name(enum_class: Type[Enum],
                   value: Optional[str],
                   fallback_value: Optional[Enum] = default,
                   value_processor=identity_deserialization_func):
    """
    Deserialize enum from it's name.

    Example:
    >>> from dataclasses_serialization.mapper.mapper import Mapper
    >>> class SampleEnum(Enum):
    ...     item1 = 'value1'
    ...     item2 = 'value2'

    >>> mapper = Mapper().register(SampleEnum, enum_to_name, enum_from_name)

    >>> mapper.deserialize(SampleEnum, 'item1')
    <SampleEnum.item1: 'value1'>
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

    Example:
    >>> from dataclasses_serialization.mapper.mapper import Mapper
    >>> class SampleEnum(Enum):
    ...     item1 = 'value1'
    ...     item2 = 'value2'

    >>> mapper = Mapper().register(SampleEnum, enum_to_value, enum_from_value)

    >>> mapper.deserialize(SampleEnum, 'value1')
    <SampleEnum.item1: 'value1'>
    """
    for enum in enum_class:
        if enum.value == value:
            return enum

    raise Exception('Unknown Enum value "%s" for class "%s"' % (value, enum_class))


def enum_to_name(item) -> str:
    """
    Serialize enum using it's name.

    Example:
    >>> from dataclasses_serialization.mapper.mapper import Mapper
    >>> class SampleEnum(Enum):
    ...     item1 = 'value1'
    ...     item2 = 'value2'

    >>> mapper = Mapper().register(SampleEnum, enum_to_name, enum_from_name)

    >>> mapper.serialize(SampleEnum.item1)
    'item1'

    """
    return item.name


def enum_to_value(item) -> Any:
    """
    Serialize enum using it's value.

    Example:
    >>> from dataclasses_serialization.mapper.mapper import Mapper
    >>> class SampleEnum(Enum):
    ...     item1 = 'value1'
    ...     item2 = 'value2'

    >>> mapper = Mapper().register(SampleEnum, enum_to_value, enum_from_value)

    >>> mapper.serialize(SampleEnum.item1)
    'value1'

    """
    return item.value
