import attrs
from toolz import curry

from dataclasses_serialization.mapper.deserialize_helpers import identity_deserialization_func
from dataclasses_serialization.mapper.serialize_helpers import keep_not_none_value
from dataclasses_serialization.serializer_base import DeserializationError, dict_serialization
from dataclasses_serialization.serializer_base.typing import (register_extension_isinstance,
                                                              register_extension_issubclass)

__all__ = [
    'attrs_serializers',
    'attrs_deserializers',
    'dict_to_attrs'
]

@register_extension_isinstance(attrs)
def attrs_isinstance(o, t):
    return attrs.has(o)


@register_extension_issubclass(attrs)
def attrs_isinstance(cls, classinfo):
    return attrs.has(cls)


@curry
def dict_to_attrs(cls,
                  dct: dict,
                  deserialization_func,
                  key_deserialization_func=identity_deserialization_func,
                  serializer=None):
    if not isinstance(dct, dict):
        raise DeserializationError(
            "Cannot deserialize {} {!r} using {}".format(
                type(dct), dct, dict_to_attrs
            )
        )

    try:
        fld_types = attrs.fields(cls)
    except TypeError:
        raise DeserializationError("Cannot deserialize unbound generic {}".format(cls))

    deserialized_key_dict = {key_deserialization_func(key): value for key, value in dct.items()}

    try:
        init_arguments = {}
        for field in fld_types:
            if field.name in deserialized_key_dict:
                init_arguments[field.name] = deserialization_func(field.type, deserialized_key_dict[field.name])

        return cls(**init_arguments)
    except TypeError as exception:
        raise DeserializationError(
            "Missing one or more required fields to deserialize {!r} as {}".format(
                dct, cls
            )
        ) from exception


def attrs_serializers(mapper, dict_post_processor=keep_not_none_value) -> dict:
    def attrs_to_dict(value):
        return dict_serialization(attrs.asdict(value),
                                  key_serialization_func=mapper._key_serializer,
                                  value_serialization_func=mapper.serialize,
                                  post_processor=dict_post_processor)

    return {
        attrs: attrs_to_dict
    }


def attrs_deserializers(mapper) -> dict:
    return {
        attrs: dict_to_attrs(deserialization_func=mapper.deserialize,
                             key_deserialization_func=mapper._key_deserializer,
                             serializer=mapper)
    }
