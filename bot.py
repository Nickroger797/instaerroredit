import os
import instaloader
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import re

from script import start_text, help_text, about_text, ai_features_text

from ai_tools.caption_extractor import extract_caption_hashtags
from ai_tools.caption_generator import generate_caption
from ai_tools.tts_caption import caption_to_audio

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
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Update Channel", url="https://t.me/yourchannel")],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
            InlineKeyboardButton("💡 About", callback_data="about"),
            InlineKeyboardButton("👤 Owner", url="https://t.me/yourusername")
        ],
        [
            InlineKeyboardButton("🧠 AI Features", callback_data="ai_features")
        ]
    ])
    await message.reply_text(start_text, reply_markup=buttons)

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
        caption = post.caption or ""

        await message.reply_video(video=video_url, caption=caption or "Instagram Reel")

        # AI Caption & Hashtag Extractor
        extracted = extract_caption_hashtags(caption)
        await message.reply_text(extracted)

        # AI Caption Generator (if no caption)
        if not caption:
            ai_caption = generate_caption(video_url)
            await message.reply_text(f"AI Generated Caption:\n{ai_caption}")

        # Text-to-Speech
        audio_file = caption_to_audio(caption)
        if audio_file:
            await message.reply_audio(audio_file, title="Caption Audio")

    except Exception as e:
        print("Error:", e)
        await message.reply_text("Failed to fetch reel. Make sure it's public.")

    await msg.delete()

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data

    if data == "about":
        await callback_query.message.edit_text(about_text, reply_markup=callback_query.message.reply_markup)
    elif data == "help":
        await callback_query.message.edit_text(help_text, reply_markup=callback_query.message.reply_markup)
    elif data == "ai_features":
        await callback_query.message.edit_text(ai_features_text, reply_markup=callback_query.message.reply_markup)

@bot.on_message(filters.command("settings") & filters.user(OWNER_ID))
async def settings(_, message: Message):
    config = await get_config()

    buttons = [
        [
            InlineKeyboardButton(f"Caption Extractor: {'✅' if config['caption_extractor'] else '❌'}", callback_data="toggle_caption_extractor"),
        ],
        [
            InlineKeyboardButton(f"Auto Caption Generator: {'✅' if config['caption_generator'] else '❌'}", callback_data="toggle_caption_generator"),
        ],
        [
            InlineKeyboardButton(f"Text-to-Speech: {'✅' if config['tts'] else '❌'}", callback_data="toggle_tts"),
        ],
        [
            InlineKeyboardButton(f"Enhancement: {'✅' if config['enhancer'] else '❌'}", callback_data="toggle_enhancer"),
        ]
    ]

    await message.reply("AI Feature Settings:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query()
async def toggle_feature(client, callback_query):
    data = callback_query.data
    key = data.replace("toggle_", "")
    config = await get_config()
    new_value = not config[key]
    await update_config(key, new_value)
    await callback_query.answer(f"{key.replace('_', ' ').title()} {'Enabled' if new_value else 'Disabled'}")
    await settings(client, callback_query.message)

bot.run()
