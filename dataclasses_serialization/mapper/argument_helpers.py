from typing import Dict, Tuple

from dataclasses_serialization.mapper.typing import SerializerMap


def merge_lazy_dicts(mapper,
                     *dicts: SerializerMap
                     ) -> Dict:
    resolved_dicts = {}
    for single_dict in dicts:

        if callable(single_dict):
            single_dict = single_dict(mapper)

        if single_dict is None:
            single_dict = {}

        try:
            resolved_dicts = {**resolved_dicts, **single_dict}
        except Exception as exception:
            print(single_dict)

    return resolved_dicts
