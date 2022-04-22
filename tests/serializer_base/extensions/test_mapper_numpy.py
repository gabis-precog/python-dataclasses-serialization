import numpy

from dataclasses_serialization.extensions.numpy_helpers import numpy_serializers, numpy_deserializers
from dataclasses_serialization.mapper.json_mapper import JsonMapper


class TestMapperNumpy:
    def setup_method(self):
        self._mapper = (JsonMapper()
                        .register_serializers(numpy_serializers)
                        .register_deserializers(numpy_deserializers)
                        )

    def test_serialize_numpy_primitive(self):
        assert self._mapper.serialize(numpy.int64(467465)) == 467465
        assert self._mapper.serialize(numpy.bool_(True)) == True
        assert self._mapper.serialize(numpy.array([[1, 2, 3], [4, 5, 6]])) == [[1, 2, 3], [4, 5, 6]]

    def test_deserialize_numpy_primitive(self):
        assert self._mapper.deserialize(numpy.int64, 467465) == numpy.int64(467465)
        assert self._mapper.deserialize(numpy.bool_, True) == numpy.bool_(True)
        numpy_array = self._mapper.deserialize(numpy.ndarray, [[1, 2, 3], [4, 5, 6]])

        assert isinstance(numpy_array, numpy.ndarray)

        assert self._mapper.serialize(numpy_array) == [[1, 2, 3], [4, 5, 6]]
