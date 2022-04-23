import inspect
import sys
import types
from dataclasses import dataclass, fields, is_dataclass
from typing import TypeVar, get_type_hints

from toolz import curry
from typing_inspect import get_args, get_generic_bases, get_origin

try:  # python < 3.7
    from typing import GenericMeta
except ImportError:
    try:  # python >= 3.9
        from typing import _GenericAlias, _SpecialForm, _SpecialGenericAlias

        GenericMeta = (_GenericAlias, _SpecialForm, _SpecialGenericAlias)
    except ImportError:  # 3.7 <= python <= 3.8
        from typing import _GenericAlias, _SpecialForm

        GenericMeta = (_GenericAlias, _SpecialForm)

if sys.version_info >= (3, 9):
    def is_generic_alias(cls):
        return isinstance(cls, types.GenericAlias)
else:
    def is_generic_alias(cls):
        return False

__all__ = [
    "is_instance",
    "is_subclass",
    "register_generic_isinstance",
    "register_generic_issubclass",
    "dataclass_field_types",
    'register_extension_isinstance',
    'register_extension_issubclass'
]

isinstance_generic_funcs = {}
issubclass_generic_funcs = {}

isinstance_extension_funcs = {}
issubclass_extension_funcs = {}


@curry
def register_generic_isinstance(origin, func):
    isinstance_generic_funcs[origin] = func

    return func


@curry
def register_generic_issubclass(origin, func):
    issubclass_generic_funcs[origin] = func

    return func


@curry
def register_extension_isinstance(origin, func):
    isinstance_extension_funcs[origin] = func

    return func


@curry
def register_extension_issubclass(origin, func):
    issubclass_extension_funcs[origin] = func

    return func


def is_instance(obj, type_):
    if type_ is dataclass:
        return not isinstance(obj, type) and is_dataclass(obj)

    if type_ in isinstance_extension_funcs:
        return isinstance_extension_funcs[type_](obj, type_)

    t_origin = get_origin(type_)

    if t_origin in isinstance_generic_funcs:
        return isinstance_generic_funcs[t_origin](obj, type_)

    return isinstance(obj, type_)


def is_subclass(cls, classinfo):
    if classinfo is dataclass:
        return isinstance(cls, type) and is_dataclass(cls)

    if cls is dataclass:
        return is_subclass(object, classinfo)

    if isinstance(cls, GenericMeta):
        origin = get_origin(cls)
        bases = get_generic_bases(origin) or (origin,)
        return classinfo in bases

    if classinfo in isinstance_extension_funcs:
        return isinstance_extension_funcs[classinfo](cls, classinfo)

    classinfo_origin = get_origin(classinfo)

    if classinfo_origin is None and isinstance(classinfo, GenericMeta):
        classinfo_origin = classinfo

    if classinfo_origin in issubclass_generic_funcs:
        return issubclass_generic_funcs[classinfo_origin](cls, classinfo)

    if is_generic_alias(cls):
        cls_origin = get_origin(cls)
        return is_subclass(cls_origin, classinfo)

    if not isinstance(cls, type):
        return False

    if not inspect.ismodule(classinfo):
        return issubclass(cls, classinfo)

    return False


@curry
def bind(bindings, generic):
    if is_instance(generic, GenericMeta):
        return generic[
            tuple(bindings[type_param] for type_param in generic.__parameters__)
        ]
    elif is_instance(generic, TypeVar):
        return bindings[generic]
    else:
        return generic


def dataclass_field_types(cls, require_bound=False):
    if not hasattr(cls, "__parameters__"):
        type_hints = get_type_hints(cls)
        flds = fields(cls)

        return ((fld, type_hints[fld.name]) for fld in flds)

    if require_bound and cls.__parameters__:
        raise TypeError("Cannot find types of unbound generic {}".format(cls))

    origin = get_origin(cls)
    type_mapping = dict(zip(origin.__parameters__, get_args(cls, evaluate=True)))

    type_hints = get_type_hints(origin)
    flds = fields(origin)

    return ((fld, bind(type_mapping, type_hints[fld.name])) for fld in flds)
