from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TestSubModel:
    a_value: str


@dataclass(frozen=True)
class TestModelTyping:
    simple_value: str
    another_value: Dict[str, str]
    more_values: List[int]
    yet_another_value: int
    ml_model: str
    sub_model: Optional[TestSubModel] = None

    def __eq__(self, o: object) -> bool:
        return self.__dict__ == o.__dict__


class SampleEnum(Enum):
    item = 'Item'


class SampleOtherEnum(Enum):
    item = '1'
    other = '2'
