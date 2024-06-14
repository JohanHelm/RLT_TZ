from datetime import datetime, timedelta

from input_data import GroupType


def date_plus_one(start_date: datetime, increment: GroupType):
    result = start_date
    hours_amount = {GroupType.HOUR: 1, GroupType.DAY: 24}
    if increment in (GroupType.HOUR, GroupType.DAY):
        result += timedelta(hours=hours_amount[increment])
    else:
        if result.month == 12:
            result = result.replace(year=result.year + 1, month=1)
        else:
            result = result.replace(month=result.month + 1)
    return result
