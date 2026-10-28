import logging
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.services.gemini_sales import gemini_sales_service
from bot.services.catalog_service import CatalogService
from bot.utils.formatters import format_currency

logger = logging.getLogger(__name__)
router = Router(name="ai_chat_router")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_user_text_chat(message: Message, session: AsyncSession, user: User, lang: str):
    user_query = message.text.strip()
    if not user_query:
        return

    # Typing indicator / status
    status_msg = await message.answer("💬 AI Maslahatchi javob tayyorlamoqda...")

    try:
        reply_text, rec_ids = await gemini_sales_service.generate_sales_response(
            session=session,
            user_message=user_query,
            user_lang=lang
        )

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

        await status_msg.delete()
        await message.answer(
            f"🤖 **AI Sotuvchi:**\n\n{reply_text}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Error in AI chat handler: {e}")
        await status_msg.edit_text(
            "Javob tayyorlashda uzilish bo'ldi. Katalog orqali qiziqtirgan tovarlarni ko'rishingiz mumkin!"
        )
