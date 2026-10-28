from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.keyboards.reply import main_menu_keyboard
from bot.keyboards.inline import language_inline_keyboard
from bot.utils.i18n import t
from bot.config import settings

router = Router(name="common_router")


@router.message(CommandStart())
async def handle_start(message: Message, user: User, lang: str, is_admin: bool):
    welcome_msg = t(
        "welcome",
        lang=lang,
        name=message.from_user.first_name or "Mijoz",
        store_name=settings.STORE_NAME
    )
    await message.answer(
        welcome_msg,
        reply_markup=main_menu_keyboard(lang=lang, is_admin=is_admin),
        parse_mode="Markdown"
    )


@router.message(F.text.in_([t("btn_lang", "uz"), t("btn_lang", "oz"), t("btn_lang", "ru")]))
@router.message(Command("til"))
async def handle_change_language(message: Message, lang: str):
    await message.answer(
        t("choose_language", lang),
        reply_markup=language_inline_keyboard()
    )


@router.callback_query(F.data.startswith("setlang:"))
async def handle_set_language_callback(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User,
    is_admin: bool
):
    selected_lang = callback.data.split(":")[1]
    user.language_code = selected_lang
    await session.commit()

    await callback.message.delete()
    confirm_text = t("lang_changed", selected_lang)
    await callback.message.answer(
        confirm_text,
        reply_markup=main_menu_keyboard(lang=selected_lang, is_admin=is_admin)
    )
    await callback.answer()


@router.message(F.text.in_([t("btn_about", "uz"), t("btn_about", "oz"), t("btn_about", "ru")]))
async def handle_about(message: Message, lang: str):
    text = t(
        "about_text",
        lang,
        store_name=settings.STORE_NAME,
        store_description=settings.STORE_DESCRIPTION,
        store_phone=settings.STORE_PHONE
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(F.text.in_([t("btn_contact", "uz"), t("btn_contact", "oz"), t("btn_contact", "ru")]))
async def handle_contact(message: Message, lang: str):
    text = t("contact_text", lang, phone=settings.STORE_PHONE)
    await message.answer(text, parse_mode="Markdown")


@router.message(F.text.in_([t("btn_ai_sales", "uz"), t("btn_ai_sales", "oz"), t("btn_ai_sales", "ru")]))
@router.callback_query(F.data == "ai_help")
async def handle_ai_consultant_entry(event: Message | CallbackQuery, lang: str):
    text = t("ai_consultant_intro", lang)
    if isinstance(event, CallbackQuery):
        await event.message.answer(text, parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, parse_mode="Markdown")
