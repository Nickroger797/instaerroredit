import os
import instaloader
from pyrogram import Client, filters
from pyrogram.types import Message
import re
import asyncio
import server  # Health check ke liye

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("insta_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
loader = instaloader.Instaloader(save_metadata=False, download_comments=False, post_metadata_txt_pattern='')

def extract_shortcode(link):
    match = re.search(r"instagram\.com/reel/([^/?\s]+)", link)
    return match.group(1) if match else None

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("Send me any public Instagram reel link!")

@bot.on_message(filters.text & ~filters.command("start"))
async def reel_downloader(_, message: Message):
    url = message.text.strip()
    shortcode = extract_shortcode(url)

    if not shortcode:
        return await message.reply_text("Invalid Instagram Reel URL.")

    msg = await message.reply_text("Downloading reel...")

    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        video_url = post.video_url

        await message.reply_video(video=video_url, caption=post.caption or "Instagram Reel")

    except Exception as e:
        print("Error:", e)
        await message.reply_text("Failed to fetch reel. Make sure it's public.")
    
    await msg.delete()

bot.run()
