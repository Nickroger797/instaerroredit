from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import re
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("reel_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
        api_url = f"https://saveig.app/api/ajaxSearch"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://saveig.app/en",
            "User-Agent": "Mozilla/5.0"
        }
        data = {"q": url}
        response = requests.post(api_url, headers=headers, data=data)
        result = response.json()

        if "links" in result and result["links"]:
            video_url = result["links"][0]["url"]
            await message.reply_video(video=video_url, caption="Here is your reel!")
        else:
            await message.reply_text("Failed to fetch the reel. Make sure the link is public.")
    except Exception as e:
        await message.reply_text("Something went wrong while downloading.")
        print(e)
    finally:
        await msg.delete()

bot.run()
