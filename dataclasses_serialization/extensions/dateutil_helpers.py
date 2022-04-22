from datetime import timedelta
from typing import Any

from dateutil.relativedelta import relativedelta

from dataclasses_serialization.mapper.deserialize_helpers import timedelta_from_milliseconds
from dataclasses_serialization.mapper.serializer_helpers import timedelta_to_milliseconds
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


def timedelta_deserialize(cls, value: Any) -> timedelta:
    if isinstance(value, timedelta):
        return value

    if isinstance(value, int):
        return timedelta_from_milliseconds(value)

    if isinstance(value, relativedelta):
        return relativedelta_to_timedelta(value)

    raise DeserializationError(
        "Cannot deserialize {} to timedelta".format(value)
    )


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
    serializers for timedelta and relativedelta
    """
    return {
        timedelta: timedelta_to_milliseconds,
        relativedelta: relativedelta_to_milliseconds
    }


def dateutil_deserializers(mapper):
    """
    deserializers for timedelta and relativedelta
    """
    return {
        timedelta: timedelta_deserialize,
        relativedelta: relativedelta_deserialize
    }

