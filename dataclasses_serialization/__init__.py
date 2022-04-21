"""
# dataclasses_serialization

`dataclasses_serialization` provides serializers/deserializers for transforming between Python dataclasses, and JSON and BSON objects.

## Basic Usage

Suppose we have the following dataclass:

>>> from dataclasses import dataclass

>>> @dataclass
... class InventoryItem:
...    name: str
...    unit_price: float
...    quantity_on_hand: int

Then we may serialize/deserialize it to/from JSON by using `dataclasses_serialization.mapper.json_mapper.JsonMapper`

>>> from dataclasses_serialization.mapper.json_mapper import JsonMapper

>>> mapper = JsonMapper()
>>> mapper.serialize(InventoryItem("Apple", 0.2, 20))
{'name': 'Apple', 'unit_price': 0.2, 'quantity_on_hand': 20}

>>> mapper.deserialize(InventoryItem, {'name': 'Apple', 'unit_price': 0.2, 'quantity_on_hand': 20})
InventoryItem(name='Apple', unit_price=0.2, quantity_on_hand=20)


## Custom Serializers

To create a custom serializer, create an instance of `dataclasses_serialization.serializer_base.Serializer`:


>>> from dataclasses_serialization.serializer_base import (
...             noop_serialization, noop_deserialization, dict_serialization,
...             dict_deserialization, list_deserialization, Serializer
...           )

>>> custom_mapper = JsonMapper(
...    serialization_functions=lambda mapper: {
...        dict: (lambda dct: dict_serialization(dct, key_serialization_func=mapper.serialize,
...                                              value_serialization_func=mapper.serialize)),
...        list: (lambda lst: list(map(mapper.serialize, lst))),
...        (str, int, float, bool, type(None)): noop_serialization
...    },
...    deserialization_functions=lambda mapper: {
...        dict: (lambda cls, dct: dict_deserialization(cls, dct, key_deserialization_func=mapper.deserialize,
...                                                     value_deserialization_func=mapper.deserialize)),
...        list: (lambda cls, lst: list_deserialization(cls, lst, deserialization_func=mapper.deserialize)),
...        (str, int, float, bool, type(None)): noop_deserialization
...    }
...  )

"""

__version__ = "1.4.0"
