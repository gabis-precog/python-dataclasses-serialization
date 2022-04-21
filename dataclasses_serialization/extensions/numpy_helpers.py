from typing import Dict

import numpy


def numpy_serializers(mapper) -> Dict:
    return {
        numpy.bool_: lambda value: bool(value),
        numpy.int64: lambda value: int(value),
        numpy.ndarray: lambda lst: list(map(mapper.serialize, lst)),
    }


def numpy_deserializers(mapper) -> Dict:
    return {
        numpy.bool_: lambda value: bool(value),
        numpy.int64: lambda value: int(value),
        numpy.ndarray: lambda lst: list(map(mapper.serialize, lst)),
    }
