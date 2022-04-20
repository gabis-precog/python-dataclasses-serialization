from datetime import timedelta
from typing import Any

from dateutil.relativedelta import relativedelta

from dataclasses_serialization.enhancements.deserialize_helpers import timedelta_from_milliseconds
from dataclasses_serialization.serializer_base.errors import DeserializationError
from dataclasses_serialization.serializer_base.typing import isinstance


def relative_delta_to_timedelta(relative_delta: relativedelta) -> timedelta:
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
        return relative_delta_to_timedelta(value)

    raise DeserializationError(
        "Cannot deserialize {} to timedelta".format(value)
    )
