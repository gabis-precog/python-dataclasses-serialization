from typing import Dict

import numpy

from dataclasses_serialization.mapper.argument_helpers import any_class_deserializer


def numpy_serializers(mapper) -> Dict:
    """
    serializers for some numpy types
    """
    return {
        numpy.bool_: lambda value: bool(value),
        numpy.int64: lambda value: int(value),
        numpy.ndarray: lambda lst: list(map(mapper.serialize, lst)),
    }


def numpy_deserializers(mapper) -> Dict:
    """
    deserializers for some numpy types
    """
    return {
        numpy.bool_: any_class_deserializer(numpy.bool_),
        numpy.int64: any_class_deserializer(numpy.int64),
        numpy.ndarray: any_class_deserializer(numpy.array),
    }
