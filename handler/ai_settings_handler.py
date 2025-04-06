# handlers/ai_settings_handler.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from ai_tools.ai_config import get_user_config, toggle_feature

@Client.on_message(filters.command("ai_settings"))
async def ai_settings_handler(bot, message: Message):
    features = await get_user_config(message.from_user.id)
    buttons = [
        [
            InlineKeyboardButton(
                f"{'✅' if features['caption_extractor'] else '❌'} Caption Extractor",
                callback_data="toggle_caption_extractor"
            ),
            InlineKeyboardButton(
                f"{'✅' if features['caption_generator'] else '❌'} Caption Generator",
                callback_data="toggle_caption_generator"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅' if features['enhancer'] else '❌'} Enhancer",
                callback_data="toggle_enhancer"
            ),
            InlineKeyboardButton(
                f"{'✅' if features['tts'] else '❌'} Text-to-Speech",
                callback_data="toggle_tts"
            )
        ]
    ]
    await message.reply_text("Choose which AI features you want to enable/disable:",
                             reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("toggle_"))
async def toggle_callback(bot, query: CallbackQuery):
    feature = query.data.replace("toggle_", "")
    status = await toggle_feature(query.from_user.id, feature)
    await query.answer(f"{feature.replace('_', ' ').title()} {'Enabled' if status else 'Disabled'}", show_alert=True)
    await ai_settings_handler(bot, query.message)
