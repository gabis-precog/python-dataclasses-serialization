import pytest

from dataclasses_serialization.enhancements.argument_helpers import merge_lazy_dicts


@pytest.mark.parametrize('dict1,dict2,expected', (
        ({'a': 1}, {'a': 2}, {'a': 2}),
        (lambda _: {'a': 1}, lambda _: {'a': 2}, {'a': 2}),
        ({'a': 1}, {'b': 2}, {'a': 1, 'b': 2}),
        (lambda _: {'a': 1}, lambda _: {'b': 2}, {'a': 1, 'b': 2}),
        ({}, {}, {}),
        (None, {}, {}),
        ({}, None, {}),
        (None, None, {}),

))
def test_merge_lazy_dicts(dict1, dict2, expected):
    assert merge_lazy_dicts(None, dict1, dict2) == expected
