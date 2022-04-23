from datetime import timedelta
from typing import Any

from dateutil.relativedelta import relativedelta

from dataclasses_serialization.mapper.serialize_helpers import timedelta_to_milliseconds
from dataclasses_serialization.serializer_base.errors import DeserializationError


def relativedelta_to_timedelta(relative_delta: relativedelta) -> timedelta:
    if isinstance(relative_delta, timedelta):
        return relative_delta

    normalized = relative_delta.normalized()

    if normalized.months != 0 or normalized.years != 0:
        raise Exception(
            'Unsupported relativedelta {}. do not use months and years. use days and weeks instead'.format(normalized))

    return timedelta(days=normalized.days,
                     hours=normalized.hours,
                     minutes=normalized.minutes,
                     seconds=normalized.seconds)


def relativedelta_from_milliseconds(value: int):
    return relativedelta(microseconds=value * 1000)


def relativedelta_to_milliseconds(value: relativedelta) -> int:
    return timedelta_to_milliseconds(relativedelta_to_timedelta(value))


def relativedelta_deserialize(cls, value: Any) -> relativedelta:
    if isinstance(value, relativedelta):
        return value

    if isinstance(value, int):
        return relativedelta_from_milliseconds(value)

    raise DeserializationError(
        "Cannot deserialize {} to timedelta".format(value)
    )


def dateutil_serializers(mapper):
    """
    serializer for relativedelta
    """
    return {
        relativedelta: relativedelta_to_milliseconds
    }


def dateutil_deserializers(mapper):
    """
    deserializer for relativedelta
    """
    return {
        relativedelta: relativedelta_deserialize
    }

