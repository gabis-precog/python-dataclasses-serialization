from dateutil.relativedelta import relativedelta

from dataclasses_serialization.extensions.dateutil_helpers import dateutil_serializers, dateutil_deserializers
from dataclasses_serialization.mapper.json_mapper import JsonMapper


class TestMapperDatetime:
    def setup_method(self):

        self._mapper = (JsonMapper()
                        .register_serializers(dateutil_serializers)
                        .register_deserializers(dateutil_deserializers)
                        )

    def test_serialize_relativedelta(self):
        assert self._mapper.serialize(relativedelta(microseconds=24000000)) == 24000

    def test_deserialize_relativedelta(self):
        assert self._mapper.deserialize(relativedelta, 24000) == relativedelta(microseconds=24000000)
