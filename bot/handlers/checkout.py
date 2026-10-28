import logging
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.services.cart_service import CartService
from bot.services.order_service import OrderService
from bot.keyboards.reply import (
    main_menu_keyboard,
    contact_keyboard,
    location_keyboard,
    payment_methods_keyboard,
    cancel_keyboard,
)
from bot.keyboards.inline import admin_order_actions_keyboard
from bot.utils.i18n import t
from bot.utils.formatters import format_currency, format_admin_order_notification
from bot.config import settings

logger = logging.getLogger(__name__)
router = Router(name="checkout_router")


class CheckoutState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()
    waiting_for_payment = State()


@router.message(F.text.in_([t("btn_cancel", "uz"), t("btn_cancel", "oz"), t("btn_cancel", "ru")]))
async def cancel_checkout(message: Message, state: FSMContext, lang: str, is_admin: bool):
    await state.clear()
    await message.answer(
        t("order_cancelled", lang),
        reply_markup=main_menu_keyboard(lang, is_admin)
    )


@router.callback_query(F.data == "start_checkout")
async def start_checkout_flow(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
    lang: str
):
    cart_items = await CartService.get_cart(session, user.id)
    if not cart_items:
        await callback.answer(t("cart_empty", lang), show_alert=True)
        return

    await state.set_state(CheckoutState.waiting_for_name)
    await callback.message.delete()

    default_name = user.full_name or ""
    await callback.message.answer(
        t("checkout_start_name", lang),
        reply_markup=cancel_keyboard(lang)
    )
    await callback.answer()


@router.message(CheckoutState.waiting_for_name)
async def process_name(message: Message, state: FSMContext, lang: str):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Iltimos, haqiqiy ismingizni kiriting:")
        return

    await state.update_data(customer_name=name)
    await state.set_state(CheckoutState.waiting_for_phone)

    await message.answer(
        t("checkout_ask_phone", lang),
        reply_markup=contact_keyboard(lang)
    )


@router.message(CheckoutState.waiting_for_phone, F.contact)
@router.message(CheckoutState.waiting_for_phone, F.text)
async def process_phone(message: Message, state: FSMContext, lang: str):
    if message.contact:
        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = "+" + phone
    else:
        phone = message.text.strip()

    await state.update_data(customer_phone=phone)
    await state.set_state(CheckoutState.waiting_for_address)

    await message.answer(
        t("checkout_ask_location", lang),
        reply_markup=location_keyboard(lang)
    )


@router.message(CheckoutState.waiting_for_address, F.location)
@router.message(CheckoutState.waiting_for_address, F.text)
async def process_address(message: Message, state: FSMContext, lang: str):
    lat, lon = None, None
    address_str = ""

    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        address_str = f"Geolokatsiya: {lat:.6f}, {lon:.6f}"
    else:
        address_str = message.text.strip()

    await state.update_data(
        delivery_address=address_str,
        latitude=lat,
        longitude=lon
    )
    await state.set_state(CheckoutState.waiting_for_payment)

    await message.answer(
        t("checkout_ask_payment", lang),
        reply_markup=payment_methods_keyboard(lang)
    )


@router.message(CheckoutState.waiting_for_payment)
async def process_payment_and_finish(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User,
    lang: str,
    is_admin: bool,
    bot: Bot
):
    text_val = message.text.lower()
    if "naqd" in text_val or "наличн" in text_val:
        payment_method = "cash"
    elif "click" in text_val:
        payment_method = "click"
    elif "payme" in text_val:
        payment_method = "payme"
    else:
        payment_method = "cash"

    data = await state.get_data()
    customer_name = data.get("customer_name", user.full_name or "Mijoz")
    customer_phone = data.get("customer_phone", "+998900000000")
    delivery_address = data.get("delivery_address", "Ko'rsatilmagan")
    lat = data.get("latitude")
    lon = data.get("longitude")

    order, err = await OrderService.create_order(
        session=session,
        user_id=user.id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        delivery_address=delivery_address,
        latitude=lat,
        longitude=lon,
        payment_method=payment_method,
        delivery_price=settings.DELIVERY_PRICE
    )

    if not order:
        await message.answer(f"Xatolik yuz berdi: {err}", reply_markup=main_menu_keyboard(lang, is_admin))
        await state.clear()
        return

    await state.clear()

    # User confirmation message
    pay_labels = {
        "cash": t("payment_cash", lang),
        "click": t("payment_click", lang),
        "payme": t("payment_payme", lang)
    }
    user_confirm = t(
        "order_confirmed",
        lang,
        order_number=order.order_number,
        total=format_currency(order.total_amount),
        phone=customer_phone,
        address=delivery_address,
        payment=pay_labels.get(payment_method, payment_method)
    )

    await message.answer(
        user_confirm,
        reply_markup=main_menu_keyboard(lang, is_admin),
        parse_mode="Markdown"
    )

    # Notify Admins
    admin_alert = format_admin_order_notification(order)
    admin_keyboard = admin_order_actions_keyboard(order.id)

    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_alert,
                reply_markup=admin_keyboard,
                parse_mode="Markdown"
            )
            # If user sent location, send it directly to admin
            if lat and lon:
                await bot.send_location(chat_id=admin_id, latitude=lat, longitude=lon)
        except Exception as e:
            logger.warning(f"Could not alert admin {admin_id}: {e}")
