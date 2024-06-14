import datetime
import os

import dotenv
import motor.motor_asyncio

from input_data import GroupType
from utils.helper import date_plus_one

dotenv.load_dotenv()


class AsyncMongoDB:
    def __init__(self):
        connection_string = os.getenv("MONGO_CONNECTION")
        client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        db = client[os.getenv("MONGO_DB_NAME")]
        self.collection = db[os.getenv("MONGO_COLLECTION_NAME")]
        self.collection.create_index("dt")

    async def salary_for_range(self, label: datetime, group_type: GroupType) -> int:
        upto = date_plus_one(label, group_type)
        cursor = self.collection.find({"dt": {"$gte": label, "$lt": upto}})
        total = 0
        async for document in cursor:
            total += document['value']
        return total
