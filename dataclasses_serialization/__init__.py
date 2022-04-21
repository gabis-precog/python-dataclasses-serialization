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

This can be used to serialize:

>>> mapper.serialize(InventoryItem("Apple", 0.2, 20))
{'name': 'Apple', 'unit_price': 0.2, 'quantity_on_hand': 20}

and deserialize:

>>> mapper.deserialize(InventoryItem, {'name': 'Apple', 'unit_price': 0.2, 'quantity_on_hand': 20})
InventoryItem(name='Apple', unit_price=0.2, quantity_on_hand=20)


## Custom Serializers

To create a custom mapper, create an instance of `dataclasses_serialization.mapper.json_mapper.JsonMapper`.
The mapping can be either overridden, or expand on the defaults.

To override the defaults completely, pass new values to **serialization_functions** and **deserialization_functions** arguments.
To leave the defaults, instantiate a JsonMapper, and supply `dataclasses_serialization.mapper.mapper.Mapper.register_serializers`
and `dataclasses_serialization.mapper.mapper.Mapper.register_deserializers` with the new mapping methods.


>>> from dataclasses_serialization.serializer_base import (
...             noop_serialization, noop_deserialization, dict_serialization,
...             dict_deserialization, list_deserialization
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
