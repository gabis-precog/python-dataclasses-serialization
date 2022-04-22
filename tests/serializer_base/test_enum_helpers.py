import pytest

from dataclasses_serialization.mapper.enum_helpers import enum_to_name, enum_to_value, enum_from_name, enum_from_value
from dataclasses_serialization.mapper.json_mapper import JsonMapper
from tests.serializer_base.fixtures import SampleEnum, SampleOtherEnum


class TestEnumHelpers:

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
            JsonMapper()
                .register_serializers(self._serializers)
                .register_deserializers(self._deserializers)
        )

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
