import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import re

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")  # Your RapidAPI Key

bot = Client("insta_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_shortcode(text):
    match = re.search(r"instagram\.com/reel/([^/?\s]+)", text)
    return match.group(1) if match else None

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("Send me any Instagram reel link, I'll download it for you!")

@bot.on_message(filters.text & ~filters.command("start"))
async def download_reel(_, message: Message):
    url = message.text
    shortcode = extract_shortcode(url)
    if not shortcode:
        return await message.reply_text("Please send a valid Instagram reel link.")

    msg = await message.reply_text("Fetching reel...")

    try:
        # Step 1: Get reel details
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "instagram230.p.rapidapi.com"
        }

        response = requests.get(
            f"https://instagram230.p.rapidapi.com/post/info?shortcode={shortcode}",
            headers=headers
        )

        json_data = response.json()
        video_url = json_data['video_url']
        caption = json_data.get("caption", "Instagram Reel")

        await message.reply_video(video_url, caption=caption)

    except Exception as e:
        await message.reply_text("Failed to fetch reel. Maybe it's private or RapidAPI error.")
        print(e)
    finally:
        await msg.delete()

bot.run()
