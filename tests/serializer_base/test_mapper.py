from collections import Counter
from datetime import timedelta
from typing import List

import pytest

from dataclasses_serialization.mapper.json_mapper import JsonMapper
from dataclasses_serialization.serializer_base.errors import DeserializationError
from tests.serializer_base.fixtures import SampleModelTyping


class TestMapper:

    def setup_method(self):
        self._mapper = JsonMapper()

    def test_deserialize_primitives(self):
        actual = self._mapper.deserialize(int, 4)

        assert actual == 4

    def test_deserialize_primitive_collection(self):
        actual = self._mapper.deserialize(List[int], [1, 3, 4])

        assert actual == [1, 3, 4]

    def test_deserialize_number_to_float(self):
        assert self._mapper.deserialize(float, 5) == 5.0
        assert self._mapper.deserialize(float, 5.0) == 5.0

        with pytest.raises(DeserializationError):
            self._mapper.deserialize(float, 'abc')

    def test_deserialize_null(self):
        assert self._mapper.deserialize(SampleModelTyping, None) is None

    def test_deserialize_timedelta(self):
        assert self._mapper.deserialize(timedelta, 24433) == timedelta(milliseconds=24433)
        assert self._mapper.deserialize(timedelta, timedelta(milliseconds=24433)) == timedelta(milliseconds=24433)

        with pytest.raises(DeserializationError):
            self._mapper.deserialize(timedelta, 'abc')

    def test_deserialize_dataclass_failure(self):
        with pytest.raises(DeserializationError):
            self._mapper.deserialize(SampleModelTyping, {})

    def test_serialize_counter(self):
        counter = Counter(a=1, b=3)
        counter.update(a=3)

        result = self._mapper.serialize(counter)

        assert result == dict(a=4, b=3)

    def test_serialize_frozenset(self):
        value = frozenset({1, 2, 3})

        serialized = self._mapper.serialize(value)

        deserialized = self._mapper.deserialize(frozenset, serialized)

        assert value == deserialized
