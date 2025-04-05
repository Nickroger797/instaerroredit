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
    match = re.search(r"instagram\\.com/reel/([^/?\\s]+)", text)
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
        print(json_data)  # Debug line added here

        video_url = json_data.get('video_url')  # Handling missing key scenario
        caption = json_data.get("caption", "Instagram Reel")

        if not video_url:
            raise ValueError("No video URL found in API response.")

        await message.reply_video(video_url, caption=caption)

    except Exception as e:
        await message.reply_text("Failed to fetch reel. Maybe it's private or RapidAPI error.")
        print(f"Error: {e}")
    finally:
        await msg.delete()

@bot.on_message(filters.command("poll_response"))
async def poll_response(_, message: Message):
    msg = await message.reply_text("Fetching poll response...")
    try:
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "real-time-instagram-scraper-api1.p.rapidapi.com"
        }
        
        response = requests.get(
            "https://real-time-instagram-scraper-api1.p.rapidapi.com/v1/poll_response?poll_id=18055206572134857&code_or_id_or_url=3592156143930432128",
            headers=headers
        )
        
        json_data = response.json()
        await message.reply_text(f"Poll Response: {json_data}")
    except Exception as e:
        await message.reply_text("Failed to fetch poll response. Check API key and request.")
        print(f"Error: {e}")
    finally:
        await msg.delete()

bot.run()
