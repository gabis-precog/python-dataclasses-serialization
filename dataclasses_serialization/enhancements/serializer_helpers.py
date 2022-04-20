from datetime import timedelta, datetime
from math import isnan, isinf
from typing import Optional


def keep_not_none_value(dct: dict) -> dict:
    return {key: value for key, value in dct.items() if value is not None}


def timedelta_to_milliseconds(td: timedelta) -> int:
    return int(td / timedelta(milliseconds=1))


def datetime_to_milliseconds(item: datetime) -> int:
    return int(item.timestamp() * 1000)


def float_serializer(value: float) -> Optional[float]:
    if isinstance(value, float):
        if isnan(value):
            return None
        if isinf(value):
            return None  # todo: is this a good idea ?
    return value


def enum_to_name(item):
    return item.name


def enum_to_value(item):
    return item.value
