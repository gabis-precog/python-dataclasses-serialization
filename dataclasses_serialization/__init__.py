"""

`dataclasses_serialization` provides serializers/deserializers for transforming between Python dataclasses, and JSON and BSON objects.

.. note::
   This documentation is for the fork at https://github.com/gabis-precog/python-dataclasses-serialization
   This project is (or aims to be) backwards compatible with the original project, So some documentation
   here may apply to (and is based on the documentation of) the original.

Basic Usage
===========

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


"""

__version__ = "1.4.0"
