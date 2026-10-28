import io
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.services.gemini_sales import gemini_sales_service
from bot.services.catalog_service import CatalogService
from bot.utils.formatters import format_currency

logger = logging.getLogger(__name__)
router = Router(name="voice_router")


@router.message(F.voice | F.audio)
async def handle_voice_message(message: Message, session: AsyncSession, user: User, lang: str, bot: Bot):
    status_msg = await message.answer("🎧 Ovozli xabaringiz eshitilmoqda va AI tahlil qilinmoqda...")

    try:
        voice = message.voice or message.audio
        file = await bot.get_file(voice.file_id)

        # Download voice into memory buffer
        voice_io = io.BytesIO()
        await bot.download_file(file.file_path, voice_io)
        voice_bytes = voice_io.getvalue()

        mime = "audio/ogg"
        if message.voice:
            mime = "audio/ogg; codecs=opus"
        elif message.audio and message.audio.mime_type:
            mime = message.audio.mime_type

        transcription, reply_text, rec_ids = await gemini_sales_service.process_voice_message(
            session=session,
            voice_bytes=voice_bytes,
            mime_type=mime,
            user_lang=lang
        )

        # Build inline buttons for recommended products
        rows = []
        if rec_ids:
            for pid in rec_ids:
                prod = await CatalogService.get_product(session, pid)
                if prod:
                    rows.append([
                        InlineKeyboardButton(
                            text=f"🛍 {prod.get_name(lang)} ({format_currency(prod.price)} so'm)",
                            callback_data=f"prod:{prod.id}"
                        ),
                        InlineKeyboardButton(
                            text="➕ Savatga",
                            callback_data=f"cart_add:{prod.id}"
                        )
                    ])

        rows.append([
            InlineKeyboardButton(text="🛒 Savatga o'tish", callback_data="view_cart"),
            InlineKeyboardButton(text="📂 Katalog", callback_data="back_categories")
        ])
        keyboard = InlineKeyboardMarkup(inline_keyboard=rows)

        final_text = (
            f"🎙 **Siz aytgan so'zlar:**\n_{transcription}_\n\n"
            f"🤖 **AI Sotuvchi Maslahatchi:**\n{reply_text}"
        )

        await status_msg.delete()
        await message.answer(final_text, reply_markup=keyboard, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error handling voice message: {e}")
        await status_msg.edit_text(
            "Ovozli xabarni qabul qilishda texnik uzilish yuz berdi. "
            "Savolingizni matn ko'rinishida yozishingiz yoki katalog orqali mahsulot tanlashingiz mumkin!"
        )
