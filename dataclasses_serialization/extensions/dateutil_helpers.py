from datetime import timedelta
from typing import Any

from dateutil.relativedelta import relativedelta

from dataclasses_serialization.mapper.deserialize_helpers import timedelta_from_milliseconds
from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.typing import is_instance


def relativedelta_to_timedelta(relative_delta: relativedelta) -> timedelta:
    if is_instance(relative_delta, timedelta):
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
    if is_instance(value, timedelta):
        return value

    if is_instance(value, int):
        return timedelta_from_milliseconds(value)

    if is_instance(value, relativedelta):
        return relativedelta_to_timedelta(value)

    raise DeserializationError(
        "Cannot deserialize {} to timedelta".format(value)
    )


def relativedelta_from_milliseconds(value):
    return relativedelta(microseconds=value * 1000)


def relativedelta_from_timedelta(value):
    pass


def relativedelta_deserialize(cls, value: Any) -> timedelta:
    if is_instance(value, relativedelta):
        return value

    if is_instance(value, int):
        return relativedelta_from_milliseconds(value)

    if is_instance(value, timedelta):
        return relativedelta_from_timedelta(value)

    raise DeserializationError(
        "Cannot deserialize {} to timedelta".format(value)
    )


def dateutil_deserializers(mapper):
    return {
        timedelta: timedelta_deserialize,
        relativedelta: relativedelta_deserialize
    }
