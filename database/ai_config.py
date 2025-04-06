# ai_tools/ai_config.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["insta_bot"]
ai_config_col = db["ai_configs"]

# Default settings
default_features = {
    "caption_extractor": True,
    "caption_generator": True,
    "enhancer": False,
    "tts": False
}

async def get_user_config(user_id: int):
    config = await ai_config_col.find_one({"user_id": user_id})
    if config:
        return config["ai_features"]
    await ai_config_col.insert_one({"user_id": user_id, "ai_features": default_features.copy()})
    return default_features.copy()

async def toggle_feature(user_id: int, feature: str):
    current = await get_user_config(user_id)
    current[feature] = not current[feature]
    await ai_config_col.update_one({"user_id": user_id}, {"$set": {"ai_features": current}})
    return current[feature]
