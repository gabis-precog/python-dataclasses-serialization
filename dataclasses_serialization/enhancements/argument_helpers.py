from typing import Optional, Dict

from dataclasses_serialization.enhancements.typing import SerializerMap


def merge_lazy_dicts(mapper,
                     dict1: Optional[SerializerMap],
                     dict2: Optional[SerializerMap] = None,
                     ) -> Dict:
    if callable(dict1):
        dict1 = dict1(mapper)

    if dict1 is None:
        dict1 = {}

    if callable(dict2):
        dict2 = dict2(mapper)

    if dict2 is None:
        dict2 = {}

    return {**dict1, **dict2}
