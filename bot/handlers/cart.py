from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.services.cart_service import CartService
from bot.services.catalog_service import CatalogService
from bot.keyboards.inline import cart_inline_keyboard, product_detail_keyboard
from bot.utils.i18n import t
from bot.utils.formatters import format_currency, format_cart_items_text
from bot.config import settings

router = Router(name="cart_router")


@router.message(F.text.in_([t("btn_cart", "uz"), t("btn_cart", "oz"), t("btn_cart", "ru")]))
@router.callback_query(F.data == "view_cart")
async def handle_view_cart(event: Message | CallbackQuery, session: AsyncSession, user: User, lang: str):
    cart_items = await CartService.get_cart(session, user.id)

    if not cart_items:
        text = t("cart_empty", lang)
        keyboard = cart_inline_keyboard([], lang=lang)
        if isinstance(event, CallbackQuery):
            if event.message.photo:
                await event.message.delete()
                await event.message.answer(text, reply_markup=keyboard)
            else:
                await event.message.edit_text(text, reply_markup=keyboard)
            await event.answer()
        else:
            await event.answer(text, reply_markup=keyboard)
        return

    subtotal, delivery, total = CartService.calculate_totals(cart_items, settings.DELIVERY_PRICE)
    items_text = format_cart_items_text(cart_items, lang=lang)

    text = t(
        "cart_title",
        lang,
        items=items_text,
        subtotal=format_currency(subtotal),
        delivery=format_currency(delivery),
        total=format_currency(total)
    )

    keyboard = cart_inline_keyboard(cart_items, lang=lang)

    if isinstance(event, CallbackQuery):
        if event.message.photo:
            await event.message.delete()
            await event.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            await event.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data.startswith("cart_add:"))
async def handle_cart_add(callback: CallbackQuery, session: AsyncSession, user: User, lang: str):
    product_id = int(callback.data.split(":")[1])
    product = await CatalogService.get_product(session, product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return

    await CartService.add_to_cart(session, user_id=user.id, product_id=product.id, quantity=1)
    new_qty = await CartService.get_item_quantity(session, user.id, product.id)

    # Refresh detail keyboard
    new_keyboard = product_detail_keyboard(
        product_id=product.id,
        category_id=product.category_id,
        lang=lang,
        cart_qty=new_qty
    )
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception:
        pass

    pname = product.get_name(lang)
    await callback.answer(t("added_to_cart", lang, product_name=pname), show_alert=False)


@router.callback_query(F.data.startswith("cart_inc:"))
async def handle_cart_inc(callback: CallbackQuery, session: AsyncSession, user: User, lang: str):
    product_id = int(callback.data.split(":")[1])
    await CartService.update_quantity(session, user.id, product_id, delta=1)
    await handle_view_cart(callback, session, user, lang)


@router.callback_query(F.data.startswith("cart_dec:"))
async def handle_cart_dec(callback: CallbackQuery, session: AsyncSession, user: User, lang: str):
    product_id = int(callback.data.split(":")[1])
    await CartService.update_quantity(session, user.id, product_id, delta=-1)
    await handle_view_cart(callback, session, user, lang)


@router.callback_query(F.data.startswith("cart_del:"))
async def handle_cart_del(callback: CallbackQuery, session: AsyncSession, user: User, lang: str):
    product_id = int(callback.data.split(":")[1])
    await CartService.remove_item(session, user.id, product_id)
    await handle_view_cart(callback, session, user, lang)


@router.callback_query(F.data == "clear_cart")
async def handle_clear_cart(callback: CallbackQuery, session: AsyncSession, user: User, lang: str):
    await CartService.clear_cart(session, user.id)
    await handle_view_cart(callback, session, user, lang)


@router.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    await callback.answer()
