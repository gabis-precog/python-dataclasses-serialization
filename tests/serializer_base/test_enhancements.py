from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import pytest

from dataclasses_serialization.enhancements.json_mapper import JsonMapper
from dataclasses_serialization.serializer_base.errors import DeserializationError


@dataclass(frozen=True)
class TestSubModel:
    a_value: str


@dataclass(frozen=True)
class TestModel:
    simple_value: str
    another_value: Dict[str, str]
    more_values: List[int]
    yet_another_value: int
    ml_model: str
    sub_model: Optional[TestSubModel] = None

    def __eq__(self, o: object) -> bool:
        return self.__dict__ == o.__dict__


class SampleEnum(Enum):
    value = 'Value'


class SampleOtherEnum(Enum):
    value = '1'
    other = '2'


class TestEnhancements:

    def setup_method(self):
        self._mapper = JsonMapper()
        # SomeEnum: lambda value: value.name,
        # SomeOtherEnum: lambda value: value.value,

    def test_deserialize_primitives(self):
        actual = self._mapper.deserialize(int, 4)

        assert actual == 4

    def test_deserialize_primitive_collection(self):
        actual = self._mapper.deserialize(List[int], [1, 3, 4])

        assert actual == [1, 3, 4]

    # def test_custom_dataclass_key_serialized(self):
    #     mapper = JsonMapper(key_serializer=camel_case)
    #
    #     result = mapper.serialize(TestModel('abc', {'a': 'b'}, [1, 2, 3], 4, 'dfg', TestSubModel('mmm')))
    #
    #     assert 'anotherValue' in result
    #     assert 'aValue' in result['subModel']

    # def test_serialize_hint(self):
    #     hint = Hint(
    #         "1234",
    #         "tag1",
    #         "tag2",
    #         DateRange(time_factory.datetime_utc_from_spec(2020, 12, 4, 10, 0),
    #                   time_factory.datetime_utc_from_spec(2020, 12, 4, 10, 0)),
    #         DateRange(time_factory.datetime_utc_from_spec(2021, 12, 4, 10, 0),
    #                   time_factory.datetime_utc_from_spec(2021, 12, 4, 10, 0), include_end=True),
    #         total_variation_historic_i=numpy.nan,
    #         log_P_of_focus_correlation_from_historic_KDE=None,
    #         kullback_leibler_i=0.6
    #     )
    #
    #     result = self._mapper.serialize(hint)
    #
    #     assert_that(result,
    #                 is_({'id': '1234', 'core_tag_id': 'tag1',
    #                      'compared_tag_id': 'tag2',
    #                      'focus_date_range': {'start': 1607076000000, 'end': 1607076000000, 'includeStart': True,
    #                                           'includeEnd': False},
    #                      'historic_date_range': {'start': 1638612000000, 'end': 1638612000000, 'includeStart': True,
    #                                              'includeEnd': True},
    #                      'kullback_leibler_i': 0.6}))
    #
    #     deserialized = self._mapper.deserialize(Hint, result)
    #
    #     assert_that(deserialized,
    #                 same_bean_as(hint).ignoring(['total_variation_historic_i']))
    #
    # def test_serialize_hint_navigation(self):
    #     navigation = HintNavigation('1234', 'abcd',
    #                                 EntityType.Investigation,
    #                                 (HintAction(HintActionTypes.Start), HintAction(HintActionTypes.Save, '1')))
    #
    #     result = self._mapper.serialize(navigation)
    #
    #     deserialized = self._mapper.deserialize(HintNavigation, result)
    #
    #     assert_that(deserialized, same_bean_as(navigation))

    def test_normalize_key_case(self):
        input = {
            'simpleValue': 'abc',
            'another-value': {'a': 'b'},
            'more_values': [1, 2, 3],
            'YetAnotherValue': 4,
            'MLModel': 'dfg'
        }
        result = self._mapper.deserialize(TestModel, input)

        assert result == TestModel('abc', {'a': 'b'}, [1, 2, 3], 4, 'dfg')

    def test_deserialize_number_to_float(self):
        assert self._mapper.deserialize(float, 5) == 5.0
        assert self._mapper.deserialize(float, 5.0) == 5.0

        with pytest.raises(DeserializationError):
            self._mapper.deserialize(float, 'abc')

    def test_deserialize_null(self):
        assert self._mapper.deserialize(TestModel, None) is None

    # def test_deserialize_timedelta(self):
    #     assert_that(self._mapper.deserialize(timedelta, 24433), is_(timedelta(milliseconds=24433)))
    #     assert_that(self._mapper.deserialize(timedelta, timedelta(milliseconds=24433)),
    #                 is_(timedelta(milliseconds=24433)))
    #     assert_that(self._mapper.deserialize(timedelta, relativedelta(microseconds=24000000)),
    #                 is_(timedelta(milliseconds=24000)))
    #
    #     assert_that(lambda: self._mapper.deserialize(timedelta, 'abc'), raises(DeserializationError))

    # def test_deserialize_hint_non_standard_field_names(self):
    #     hint_data = {'id': '901372f9-c1d5-440b-9d63-f3362dd96d92', 'core_tag_id': '12186', 'compared_tag_id': '12186',
    #                  'focus_date_range': {'start': 1618312680000, 'end': 1618399080000, 'includeStart': True,
    #                                       'includeEnd': False},
    #                  'historic_date_range': {'start': 1618226280000, 'end': 1618312680000, 'includeStart': True,
    #                                          'includeEnd': False}, 'created_at': 1637586700296,
    #                  'score': 1.5200710284555483e-05, 'last_feedback': None,
    #                  'jensen_shannon_2D': 0.045066787590019225}
    #
    #     hint = self._mapper.deserialize(Hint, hint_data)
    #     assert_that(hint.jensen_shannon_2D, is_(0.045066787590019225))

    # @pytest.mark.parametrize('enum_type, value, expected_enum', (
    #         (FieldActivityType, 'Mute', FieldActivityType.Mute),
    #         (FieldActivityType, 'Undefined', FieldActivityType.Other),
    #
    #         (MessageTaskType, 'FieldActivity', MessageTaskType.field_activity),
    #         (MessageTaskType, 'field_activity', MessageTaskType.field_activity),
    #
    #         (ConditionOperator, '<', ConditionOperator.lt),
    #         (ConditionOperator, '>=', ConditionOperator.ge),
    # ))
    # def test_deserialize_enums(self, enum_type, value, expected_enum):
    #     assert_that(self._mapper.deserialize(enum_type, value), is_(expected_enum))

    @pytest.mark.parametrize('enum_type, value', (
            (SampleEnum, 'NonExisting'),
    ))
    def test_deserialize_enums_failure(self, enum_type, value):
        with pytest.raises(Exception):
            self._mapper.deserialize(enum_type, value)

    def test_deserialize_dataclass_failure(self):
        with pytest.raises(DeserializationError):
            self._mapper.deserialize(TestModel, {})

    def test_serialize_counter(self):
        counter = Counter(a=1, b=3)
        counter.update(a=3)

        result = self._mapper.serialize(counter)

        assert result == dict(a=4, b=3)

    @pytest.mark.skip
    def test_serialize_frozenset(self):
        value = frozenset({1, 2, 3})

        serialized = self._mapper.serialize(value)

        deserialized = self._mapper.deserialize(frozenset, serialized)

        assert value == deserialized
