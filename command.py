from pyrogram import filters
from handler.ai_settings_handler import ai_settings_handler, toggle_callback

def register_handlers(bot):
    @bot.on_message(filters.command("ai_settings"))
    async def handle_ai_settings(client, message):
        await ai_settings_handler(client, message)

    @bot.on_callback_query(filters.regex("toggle_"))
    async def handle_toggle_callback(client, callback_query):
        await toggle_callback(client, callback_query)
