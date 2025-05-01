import os
import motor.motor_asyncio
from beanie import init_beanie
from bson.objectid import ObjectId

from .models.model import BookModel


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        os.environ["DB_URL"]
    )

    await init_beanie(database=client.db_name, document_models=[BookModel])
