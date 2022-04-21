import numpy

serializers = {
    numpy.bool_: lambda value: bool(value),
    numpy.int64: lambda value: int(value),
    # numpy.ndarray: lambda lst: list(map(self.serialize, lst)),
}
