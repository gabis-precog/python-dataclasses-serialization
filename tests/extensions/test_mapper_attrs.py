from typing import Dict

from attr import define

from dataclasses_serialization.extensions.attrs_helpers import attrs_serializers, attrs_deserializers
from dataclasses_serialization.mapper.json_mapper import JsonMapper


@define
class SampleAttrs:
    number: int
    name: str
    lookup: Dict[str, int]


class TestMapperDatetime:
    def setup_method(self):
        self._mapper = (JsonMapper()
                        .register_serializers(attrs_serializers)
                        .register_deserializers(attrs_deserializers)
                        )

    def test_serialize_attrs(self):
        item = SampleAttrs(3, 'a', {'b': 2})
        assert self._mapper.serialize(item) == {'number': 3, 'name': 'a', 'lookup': {'b': 2}}

    def test_deserialize_attrs(self):
        item = {'number': 3, 'name': 'a', 'lookup': {'b': 2}}
        assert self._mapper.deserialize(SampleAttrs, item) == SampleAttrs(3, 'a', {'b': 2})
