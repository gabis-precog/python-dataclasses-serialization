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
        numpy.bool_: lambda cls, value: numpy.bool_(value),
        numpy.int64: lambda cls, value: numpy.int64(value),
        numpy.ndarray: lambda cls, value: numpy.array(value),
    }
