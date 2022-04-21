from pydash import camel_case

from dataclasses_serialization.mapper.json_mapper import JsonMapper


class JavaJsonMapper(JsonMapper):
    def __init__(self):
        super().__init__(key_serializer=camel_case)
