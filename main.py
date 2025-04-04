from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import re
import os
from bs4 import BeautifulSoup

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("igram_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_instagram_url(text):
    regex = r"(https?://www\.instagram\.com/reel/[^\s]+)"
    match = re.search(regex, text)
    return match.group(1) if match else None

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("Hi! Send me any public Instagram reel link and I'll download it for you.")

@bot.on_message(filters.text & ~filters.command("start"))
async def reel_downloader(_, message: Message):
    url = extract_instagram_url(message.text)
    if not url:
        return await message.reply_text("Please send a valid Instagram reel link.")

    msg = await message.reply_text("Downloading reel...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"url": url}
        response = requests.post("https://igram.io/i/", headers=headers, data=data)
        soup = BeautifulSoup(response.text, "html.parser")
        video_link = soup.find("a", {"class": "btn btn-light"})["href"]

        await message.reply_video(video=video_link, caption="Here is your reel!")
    except Exception as e:
        await message.reply_text("Failed to download. Make sure the link is public.")
        print(e)
    finally:
        await msg.delete()

bot.run()
