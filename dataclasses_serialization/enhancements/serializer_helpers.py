from datetime import timedelta, datetime


def keep_not_none_value(dct: dict) -> dict:
    return {key: value for key, value in dct.items() if value is not None}


def timedelta_to_milliseconds(td: timedelta) -> int:
    return int(td / timedelta(milliseconds=1))


def datetime_to_milliseconds(item: datetime) -> int:
    return int(item.timestamp() * 1000)
