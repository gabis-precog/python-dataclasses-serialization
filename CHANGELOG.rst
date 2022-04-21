.. _changelog:

Changelog
=========


v1.4.0 (TBA))
-------------------

- Dropped support for python 3.6 (End of life), removed **dataclass** library dependency
- Support python >= 3.9 generics (list, dict, set)
- Support **frozenset**
- Sample mapping for Support **Enum** mapping
- Sample mapping for **datetime** and **timedelta**
- Extension support: **numpy**
- Extension support: key mapping for python and java conventions
- Extension support: **relativedelta**
- Added **JsonMapper** and **BsonMapper** to instantiate and customize mappers instead of using global single instance
- de/serialization function map can now be passed as a callable which accepts the current mapper as an argument. Allow for proper subclassing and using self internally instead of a static class

Implementation changes:

- Do not overload builtin **isinstance** and **issubclass**
- Do not overload **get_args**

