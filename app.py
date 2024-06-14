import json
from datetime import datetime

from input_data import InputData, GroupType
from db.motor_db import AsyncMongoDB
from utils.helper import date_plus_one


class DataAgregator:
    def __init__(self, input_text: str):
        self.input_text = input_text
        self.input_data: InputData | None = None
        self.labels: list[datetime | None] = []
        self.result: dict[str, list[int | str]] = {"dataset": [], "labels": []}
        self.async_mongo_db = AsyncMongoDB()

    def create_input_data_obj(self):
        input_dict = json.loads(self.input_text)
        input_data = InputData(datetime.fromisoformat(input_dict["dt_from"]),
                               datetime.fromisoformat(input_dict["dt_upto"]),
                               GroupType.create_group_type(input_dict["group_type"])
                               )
        self.input_data = input_data

    def create_labels_range(self):
        process_date = self.input_data.dt_from
        while process_date < self.input_data.dt_upto:
            self.labels.append(process_date)
            process_date = date_plus_one(process_date, self.input_data.group_type)

    async def agregate(self):
        for label in self.labels:
            self.result["dataset"].append(await self.async_mongo_db.salary_for_range(label, self.input_data.group_type))
            self.result["labels"].append(label.isoformat())

    async def execute(self):
        try:
            self.create_input_data_obj()
            self.create_labels_range()
            await self.agregate()
            return self.result
        except Exception as err:
            return "Ошибка во входных данных"
