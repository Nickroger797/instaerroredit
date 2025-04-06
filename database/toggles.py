from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["ai_bot"]
config_col = db["config"]

DEFAULT_CONFIG = {
    "caption_extractor": True,
    "caption_generator": True,
    "tts": True,
    "enhancer": False
}

async def get_config():
    config = await config_col.find_one({"_id": "bot_config"})
    if not config:
        await config_col.insert_one({"_id": "bot_config", **DEFAULT_CONFIG})
        config = await config_col.find_one({"_id": "bot_config"})
    return config

async def update_config(key, value):
    await config_col.update_one({"_id": "bot_config"}, {"$set": {key: value}})
