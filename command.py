from pyrogram import filters, handlers
from handler.ai_settings_handler import ai_settings_handler, toggle_callback
from bot import bot

# Registering the command handler
bot.add_handler(handlers.MessageHandler(ai_settings_handler, filters.command("ai_settings")))

# Registering the callback query handler
bot.add_handler(handlers.CallbackQueryHandler(toggle_callback, filters.regex("toggle_")))
