from pydash import camel_case

from dataclasses_serialization.extensions.key_helpers import normalize_key_case
from dataclasses_serialization.mapper.json_mapper import JsonMapper
from tests.serializer_base.fixtures import SampleModelTyping, SampleSubModel


class TestMapperKeys:

    def setup_method(self):
        self._mapper = JsonMapper(key_deserializer=normalize_key_case)

    def test_custom_dataclass_key_serialized(self):
        mapper = self._mapper = JsonMapper(key_serializer=camel_case)

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
