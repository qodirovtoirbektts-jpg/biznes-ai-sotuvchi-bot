import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User, Category, Product, StoreSetting
from bot.services.order_service import OrderService
from bot.services.catalog_service import CatalogService
from bot.keyboards.inline import (
    admin_panel_inline_keyboard,
    admin_order_actions_keyboard,
)
from bot.keyboards.reply import main_menu_keyboard
from bot.utils.i18n import t, get_status_label
from bot.utils.formatters import format_currency, format_admin_order_notification

logger = logging.getLogger(__name__)
router = Router(name="admin_router")


class AddProductState(StatesGroup):
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_description = State()
    waiting_for_photo = State()


class EditPromptState(StatesGroup):
    waiting_for_new_prompt = State()


@router.message(Command("admin"))
@router.message(F.text.in_([t("btn_admin_panel", "uz"), t("btn_admin_panel", "oz"), t("btn_admin_panel", "ru")]))
async def handle_admin_entry(message: Message, is_admin: bool):
    if not is_admin:
        await message.answer("Kechirasiz, ushbu bo'lim faqat do'kon ma'murlari (admin) uchun ochiq.")
        return

    text = (
        "👑 **\"Biznes AI Sotuvchi\" — Boshqaruv Paneli**\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )
    await message.answer(text, reply_markup=admin_panel_inline_keyboard(), parse_mode="Markdown")


@router.callback_query(F.data == "admin_stats")
async def handle_admin_stats(callback: CallbackQuery, session: AsyncSession, is_admin: bool):
    if not is_admin:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    stats = await OrderService.get_statistics(session)

    text = (
        "📊 **DO'KON SAVDO STATISTIKASI:**\n\n"
        f"📅 **Bugun:**\n"
        f"  • Buyurtmalar: {stats['today_orders']} ta\n"
        f"  • Savdo tushumi: **{format_currency(stats['today_revenue'])} so'm**\n\n"
        f"📦 **Jami ko'rsatkichlar:**\n"
        f"  • Barcha buyurtmalar: {stats['total_orders']} ta\n"
        f"  • Jami savdo tushumi: **{format_currency(stats['total_revenue'])} so'm**\n"
        f"  • Yangi kutilayotgan: **{stats['pending_orders']} ta**"
    )
    await callback.message.edit_text(text, reply_markup=admin_panel_inline_keyboard(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_orders:"))
async def handle_admin_orders_list(callback: CallbackQuery, session: AsyncSession, is_admin: bool):
    if not is_admin:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    status = callback.data.split(":")[1]
    orders = await OrderService.get_orders_by_status(session, status, limit=10)

    if not orders:
        await callback.message.edit_text(
            f"ℹ️ '{status}' holatidagi buyurtmalar hozircha yo'q.",
            reply_markup=admin_panel_inline_keyboard()
        )
        await callback.answer()
        return

    await callback.message.delete()
    for order in orders:
        order_text = format_admin_order_notification(order)
        keyboard = admin_order_actions_keyboard(order.id)
        await callback.message.answer(order_text, reply_markup=keyboard, parse_mode="Markdown")

    await callback.answer()


@router.callback_query(F.data.startswith("adm_status:"))
async def handle_admin_status_change(callback: CallbackQuery, session: AsyncSession, is_admin: bool, bot: Bot):
    if not is_admin:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    parts = callback.data.split(":")
    order_id = int(parts[1])
    new_status = parts[2]

    order = await OrderService.update_order_status(session, order_id, new_status)
    if not order:
        await callback.answer("Buyurtma topilmadi!", show_alert=True)
        return

    status_lbl = get_status_label(new_status, "uz")
    await callback.answer(f"Holat yangilandi: {status_lbl}")

    # Notify customer via Telegram
    try:
        user_lang = order.user.language_code if order.user else "uz"
        notify_text = t(
            "status_updated_notify",
            user_lang,
            order_number=order.order_number,
            status=get_status_label(new_status, user_lang)
        )
        await bot.send_message(chat_id=order.user_id, text=notify_text, parse_mode="Markdown")
    except Exception as e:
        logger.warning(f"Could not notify customer {order.user_id}: {e}")

    # Update admin card
    updated_text = format_admin_order_notification(order)
    keyboard = admin_order_actions_keyboard(order.id)
    try:
        await callback.message.edit_text(updated_text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception:
        pass


@router.callback_query(F.data == "admin_add_product")
async def start_add_product_flow(callback: CallbackQuery, state: FSMContext, session: AsyncSession, is_admin: bool):
    if not is_admin:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    categories = await CatalogService.get_categories(session)
    if not categories:
        await callback.answer("Oldin kategoriya yaratish kerak!", show_alert=True)
        return

    rows = []
    for cat in categories:
        rows.append([InlineKeyboardButton(text=f"📁 {cat.name_uz}", callback_data=f"adm_sel_cat:{cat.id}")])
    rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm_cancel_fsm")])

    await state.set_state(AddProductState.waiting_for_category)
    await callback.message.edit_text(
        "➕ **Yangi mahsulot qo'shish:**\nQaysi kategoriyaga qo'shmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(AddProductState.waiting_for_category, F.data.startswith("adm_sel_cat:"))
async def process_add_prod_category(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split(":")[1])
    await state.update_data(category_id=cat_id)
    await state.set_state(AddProductState.waiting_for_name)

    await callback.message.edit_text(
        "📝 Mahsulot nomini kiriting (masalan: `iPhone 16 Pro 128GB`):",
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(AddProductState.waiting_for_name)
async def process_add_prod_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name_uz=name)
    await state.set_state(AddProductState.waiting_for_price)

    await message.answer("💰 Mahsulot narxini so'mda faqat raqamlar bilan kiriting (masalan: `12500000`):")


@router.message(AddProductState.waiting_for_price)
async def process_add_prod_price(message: Message, state: FSMContext):
    raw_val = message.text.replace(" ", "").replace(",", "").strip()
    if not raw_val.isdigit():
        await message.answer("Iltimos, narxni faqat butun musbat raqam ko'rinishida yozing:")
        return

    price = int(raw_val)
    await state.update_data(price=price)
    await state.set_state(AddProductState.waiting_for_description)

    await message.answer("📋 Mahsulot tavsifini kiriting (xususiyatlari, kafolati va h.k.):")


@router.message(AddProductState.waiting_for_description)
async def process_add_prod_desc(message: Message, state: FSMContext):
    desc = message.text.strip()
    await state.update_data(description=desc)
    await state.set_state(AddProductState.waiting_for_photo)

    await message.answer(
        "🖼 Mahsulot rasmini yuboring (yoki rasm bo'lmasa `o'tkazish` deb yozing):",
        parse_mode="Markdown"
    )


@router.message(AddProductState.waiting_for_photo)
async def process_add_prod_photo_and_save(message: Message, state: FSMContext, session: AsyncSession, is_admin: bool):
    photo_url = None
    if message.photo:
        photo_url = message.photo[-1].file_id
    elif message.text and "o'tkaz" in message.text.lower():
        photo_url = None

    data = await state.get_data()
    new_product = Product(
        category_id=data["category_id"],
        name_uz=data["name_uz"],
        price=data["price"],
        description=data["description"],
        image_url=photo_url,
        stock=50,
        is_active=True
    )
    session.add(new_product)
    await session.commit()
    await state.clear()

    await message.answer(
        f"✅ **'{new_product.name_uz}'** mahsuloti muvaffaqiyatli saqlandi va katalogga qo'shildi!",
        reply_markup=main_menu_keyboard(is_admin=is_admin),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "admin_ai_prompt")
async def handle_admin_ai_prompt_view(callback: CallbackQuery, session: AsyncSession, is_admin: bool):
    if not is_admin:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    result = await session.execute(select(StoreSetting).where(StoreSetting.key == "ai_system_prompt"))
    row = result.scalars().first()
    curr_prompt = row.value if row else "Standart tizim yo'riqnomasi"

    text = (
        "🤖 **AI Sotuvchi Maslahatchi — System Prompt:**\n\n"
        f"_{curr_prompt}_\n\n"
        "O'zgartirish uchun yangi prompt matnini to'g'ridan-to'g'ri yozib yuborishingiz mumkin."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ O'zgartirish", callback_data="adm_edit_prompt")],
        [InlineKeyboardButton(text="⬅️ Panelga qaytish", callback_data="adm_back_panel")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "adm_edit_prompt")
async def start_edit_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditPromptState.waiting_for_new_prompt)
    await callback.message.edit_text(
        "📝 AI sotuvchi uchun yangi yo'riqnoma (System Prompt) matnini yozing:\n"
        "(Bekor qilish uchun `/cancel` deb yozing)"
    )
    await callback.answer()


@router.message(EditPromptState.waiting_for_new_prompt)
async def save_new_prompt(message: Message, state: FSMContext, session: AsyncSession, is_admin: bool):
    new_text = message.text.strip()
    result = await session.execute(select(StoreSetting).where(StoreSetting.key == "ai_system_prompt"))
    row = result.scalars().first()
    if row:
        row.value = new_text
    else:
        session.add(StoreSetting(key="ai_system_prompt", value=new_text))
    await session.commit()
    await state.clear()

    await message.answer(
        "✅ AI sotuvchi yo'riqnomasi muvaffaqiyatli yangilandi!",
        reply_markup=main_menu_keyboard(is_admin=is_admin)
    )


@router.callback_query(F.data == "adm_back_panel")
async def back_to_admin_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "👑 **\"Biznes AI Sotuvchi\" — Boshqaruv Paneli**",
        reply_markup=admin_panel_inline_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "adm_cancel_fsm")
async def cancel_admin_fsm(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await back_to_admin_panel(callback)
