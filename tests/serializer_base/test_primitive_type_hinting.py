import sys
from dataclasses import dataclass
from typing import Optional

import pytest

from dataclasses_serialization.enhancements.json_mapper import JsonMapper
from dataclasses_serialization.enhancements.key_helpers import normalize_key_case
from tests.serializer_base.fixtures import TestSubModel

try:
    if sys.version_info > (3, 8):
        @dataclass(frozen=True)
        class TestModelPrimitive:
            simple_value: str
            another_value: dict[str, str]
            more_values: list[int]
            yet_another_value: int
            ml_model: str
            sub_model: Optional[TestSubModel] = None

            def __eq__(self, o: object) -> bool:
                return self.__dict__ == o.__dict__


        @pytest.mark.skip
        def test_deserialize_primitive_types():
            serialized = {
                'simpleValue': 'abc',
                'another-value': {'a': 'b'},
                'more_values': [1, 2, 3],
                'YetAnotherValue': 4,
                'MLModel': 'dfg'
            }
            result = JsonMapper(key_serializer=normalize_key_case).deserialize(TestModelPrimitive, serialized)

            assert result == TestModelPrimitive('abc', {'a': 'b'}, [1, 2, 3], 4, 'dfg')

except Exception:
    pass
