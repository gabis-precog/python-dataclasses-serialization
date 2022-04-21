from collections import Counter
from datetime import timedelta
from typing import List

import pytest
from pydash import camel_case

from dataclasses_serialization.mapper.enum_helpers import enum_to_name, enum_to_value, enum_from_name, enum_from_value
from dataclasses_serialization.mapper.json_mapper import JsonMapper
from dataclasses_serialization.extensions.key_helpers import normalize_key_case
from dataclasses_serialization.serializer_base.errors import DeserializationError
from tests.serializer_base.fixtures import SampleEnum, SampleOtherEnum, SampleModelTyping, SampleSubModel


class TestMapper:

    def setup_method(self):
        self._serializers = {
            SampleEnum: enum_to_name,
            SampleOtherEnum: enum_to_value,
        }
        self._deserializers = {
            SampleEnum: enum_from_name,
            SampleOtherEnum: enum_from_value
        }

        self._mapper = (
            JsonMapper(key_deserializer=normalize_key_case)
                .register_serializers(self._serializers)
                .register_deserializers(self._deserializers)
        )

    def test_deserialize_primitives(self):
        actual = self._mapper.deserialize(int, 4)

        assert actual == 4

    def test_deserialize_primitive_collection(self):
        actual = self._mapper.deserialize(List[int], [1, 3, 4])

        assert actual == [1, 3, 4]

    def test_custom_dataclass_key_serialized(self):
        mapper = self._mapper = (
            JsonMapper(key_serializer=camel_case)
                .register_serializers(self._serializers)
                .register_deserializers(self._deserializers)
        )

        result = mapper.serialize(SampleModelTyping('abc', {'a': 'b'}, [1, 2, 3], 4, 'dfg', SampleSubModel('mmm')))

        assert 'anotherValue' in result
        assert 'aValue' in result['subModel']

    def test_normalize_key_case(self):
        serialized = {
            'simpleValue': 'abc',
            'another-value': {'a': 'b'},
            'more_values': [1, 2, 3],
            'YetAnotherValue': 4,
            'MLModel': 'dfg'
        }
        result = self._mapper.deserialize(SampleModelTyping, serialized)

        assert result == SampleModelTyping('abc', {'a': 'b'}, [1, 2, 3], 4, 'dfg')

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
        # assert self._mapper.deserialize(timedelta, relativedelta(microseconds=24000000)) == timedelta(
        #     milliseconds=24000)

        with pytest.raises(DeserializationError):
            self._mapper.deserialize(timedelta, 'abc')

    @pytest.mark.parametrize('enum_type, value, expected_enum', (
            (SampleEnum, 'item', SampleEnum.item),
            (SampleOtherEnum, '1', SampleOtherEnum.item),
            (SampleOtherEnum, '2', SampleOtherEnum.other),
    ))
    def test_deserialize_enums(self, enum_type, value, expected_enum):
        assert self._mapper.deserialize(enum_type, value) == expected_enum

    @pytest.mark.parametrize('enum_value, expected_value', (
            (SampleEnum.item, 'item'),
            (SampleOtherEnum.item, '1'),
            (SampleOtherEnum.other, '2'),

    ))
    def test_serialize_enums(self, enum_value, expected_value):
        assert self._mapper.serialize(enum_value) == expected_value

    @pytest.mark.parametrize('enum_type, value', (
            (SampleEnum, 'NonExisting'),
    ))
    def test_deserialize_enums_failure(self, enum_type, value):
        with pytest.raises(Exception):
            self._mapper.deserialize(enum_type, value)

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
