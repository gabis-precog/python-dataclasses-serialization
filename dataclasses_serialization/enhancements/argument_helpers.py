from typing import Any, Callable, Optional, Union


def merge_lazy_dicts(mapper,
                     dict1: Optional[Union[dict, Callable[[Any], dict]]],
                     dict2: Optional[Union[dict, Callable[[Any], dict]]] = None,
                     ) -> dict:
    if callable(dict1):
        dict1 = dict1(mapper)

    if dict1 is None:
        dict1 = {}

    if callable(dict2):
        dict2 = dict2(mapper)

    if dict2 is None:
        dict2 = {}

    return {**dict1, **dict2}
