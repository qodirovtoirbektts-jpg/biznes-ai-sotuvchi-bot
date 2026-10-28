from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User
from bot.services.catalog_service import CatalogService
from bot.services.cart_service import CartService
from bot.services.gemini_sales import gemini_sales_service
from bot.keyboards.inline import (
    categories_inline_keyboard,
    products_inline_keyboard,
    product_detail_keyboard,
)
from bot.utils.i18n import t
from bot.utils.formatters import format_currency

router = Router(name="catalog_router")


@router.message(F.text.in_([t("btn_catalog", "uz"), t("btn_catalog", "oz"), t("btn_catalog", "ru")]))
@router.callback_query(F.data == "back_categories")
async def show_categories(event: Message | CallbackQuery, session: AsyncSession, lang: str):
    categories = await CatalogService.get_categories(session)
    text = t("categories_title", lang)
    keyboard = categories_inline_keyboard(categories, lang=lang)

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data.startswith("cat:"))
async def show_products_in_category(callback: CallbackQuery, session: AsyncSession, lang: str):
    category_id = int(callback.data.split(":")[1])
    category = await CatalogService.get_category(session, category_id)
    products = await CatalogService.get_products_by_category(session, category_id)

    cat_name = category.get_name(lang) if category else "Bo'lim"

    if not products:
        empty_text = t("empty_category", lang)
        keyboard = categories_inline_keyboard([category] if category else [], lang=lang)
        await callback.message.edit_text(empty_text, reply_markup=keyboard)
        await callback.answer()
        return

    title = t("products_in_category", lang, category=cat_name)
    keyboard = products_inline_keyboard(products, category_id=category_id, lang=lang)
    await callback.message.edit_text(title, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("prod:"))
async def show_product_details(callback: CallbackQuery, session: AsyncSession, user: User, lang: str):
    product_id = int(callback.data.split(":")[1])
    product = await CatalogService.get_product(session, product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return

    cart_qty = await CartService.get_item_quantity(session, user_id=user.id, product_id=product.id)
    pname = product.get_name(lang)
    price_str = format_currency(product.price)
    desc = product.description or "Tavsif berilmagan."

    card_text = t(
        "product_details",
        lang,
        name=pname,
        description=desc,
        price=price_str,
        stock=product.stock
    )

    keyboard = product_detail_keyboard(
        product_id=product.id,
        category_id=product.category_id,
        lang=lang,
        cart_qty=cart_qty
    )

    # If product has photo, we can send photo or edit caption
    if product.image_url and product.image_url.startswith("http"):
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=product.image_url,
                caption=card_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            await callback.answer()
            return
        except Exception:
            pass  # Fallback to text message if photo fails

    await callback.message.edit_text(card_text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("ai_ask_prod:"))
async def handle_ai_ask_product(callback: CallbackQuery, session: AsyncSession, lang: str):
    product_id = int(callback.data.split(":")[1])
    product = await CatalogService.get_product(session, product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return

    await callback.answer("AI tahlil qilmoqda...")
    pname = product.get_name(lang)
    query = f"Men '{pname}' mahsuloti haqida ko'proq bilmoqchiman. Uning asosiy afzalliklari nimada va nima uchun uni sotib olishim kerak?"

    resp, rec_ids = await gemini_sales_service.generate_sales_response(
        session=session,
        user_message=query,
        user_lang=lang
    )

    await callback.message.answer(f"🤖 **AI Maslahatchi:**\n\n{resp}", parse_mode="Markdown")
