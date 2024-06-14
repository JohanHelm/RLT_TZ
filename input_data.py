from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class GroupType(Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"

    @classmethod
    def create_group_type(cls, text_group_type: str):
        for group_type in cls:
            if group_type.value == text_group_type:
                return group_type


@dataclass
class InputData:
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupType
