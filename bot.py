import os
import re
import instaloader
from pyrogram import Client, filters
from pyrogram.types import Message

# अपने Telegram API क्रेडेंशियल्स यहाँ भरें
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("insta_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Instaloader सेटअप
L = instaloader.Instaloader()

def extract_shortcode(text):
    match = re.search(r"instagram\.com/reel/([^/?\s]+)", text)
    return match.group(1) if match else None

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("मुझे कोई भी Instagram रील लिंक भेजें, मैं उसे आपके लिए डाउनलोड करूंगा!")

@bot.on_message(filters.text & ~filters.command("start"))
async def download_reel(_, message: Message):
    url = message.text
    shortcode = extract_shortcode(url)
    if not shortcode:
        return await message.reply_text("कृपया एक वैध Instagram रील लिंक भेजें।")

    msg = await message.reply_text("रील प्राप्त की जा रही है...")

    try:
        # रील डाउनलोड करें
        L.download_post(L.check_shortcode(shortcode), target=shortcode)
        video_path = f"{shortcode}/{shortcode}.mp4"

        if os.path.exists(video_path):
            await message.reply_video(video_path, caption="यहाँ आपकी रील है!")
            os.remove(video_path)
            os.rmdir(shortcode)
        else:
            await message.reply_text("रील डाउनलोड करने में असफल। शायद यह निजी है या कोई अन्य समस्या है।")

    except Exception as e:
        await message.reply_text(f"त्रुटि: {str(e)}")
    finally:
        await msg.delete()

bot.run()
