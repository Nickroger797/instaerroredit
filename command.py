# commands/ai_settings.py
from pyrogram import filters
from handlers.ai_settings_handler import ai_settings_handler, toggle_callback
from bot import bot

bot.add_handler(
    pyrogram.handlers.MessageHandler(ai_settings_handler, filters.command("ai_settings"))
)

bot.add_handler(
    pyrogram.handlers.CallbackQueryHandler(toggle_callback, filters.regex("toggle_"))
)
