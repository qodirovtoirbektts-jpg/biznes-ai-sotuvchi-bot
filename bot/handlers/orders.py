from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.services.order_service import OrderService
from bot.utils.i18n import t
from bot.utils.formatters import format_order_summary

router = Router(name="orders_router")


@router.message(F.text.in_([t("btn_orders", "uz"), t("btn_orders", "oz"), t("btn_orders", "ru")]))
async def handle_user_orders(message: Message, session: AsyncSession, user: User, lang: str):
    orders = await OrderService.get_user_orders(session, user.id, limit=5)

    if not orders:
        if lang == "ru":
            await message.answer("📦 У вас пока нет оформленных заказов. Перейдите в каталог, чтобы сделать первый заказ!")
        else:
            await message.answer("📦 Sizda hozircha buyurtmalar mavjud emas. Katalogga o'tib dastlabki buyurtmangizni bering!")
        return

    for order in orders:
        summary_text = format_order_summary(order, lang=lang)
        await message.answer(summary_text, parse_mode="Markdown")
