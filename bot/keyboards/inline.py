from typing import List, Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.database.models import Category, Product, CartItem
from bot.utils.i18n import t


def language_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha (Lotin)", callback_data="setlang:uz"),
                InlineKeyboardButton(text="🇺🇿 Ўзбекча (Кирилл)", callback_data="setlang:oz"),
            ],
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang:ru"),
            ]
        ]
    )


def categories_inline_keyboard(categories: List[Category], lang: str = "uz") -> InlineKeyboardMarkup:
    rows = []
    for cat in categories:
        name = cat.get_name(lang)
        rows.append([InlineKeyboardButton(text=f"📁 {name}", callback_data=f"cat:{cat.id}")])

    rows.append([
        InlineKeyboardButton(text="🛒 Savatga o'tish", callback_data="view_cart"),
        InlineKeyboardButton(text="💬 AI Maslahatchi", callback_data="ai_help"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def products_inline_keyboard(products: List[Product], category_id: int, lang: str = "uz") -> InlineKeyboardMarkup:
    rows = []
    for prod in products:
        pname = prod.get_name(lang)
        price_k = f"{prod.price:,}".replace(",", " ")
        rows.append([
            InlineKeyboardButton(
                text=f"{pname} • {price_k} so'm",
                callback_data=f"prod:{prod.id}"
            )
        ])

    rows.append([
        InlineKeyboardButton(text="⬅️ Bo'limlarga qaytish", callback_data="back_categories"),
        InlineKeyboardButton(text="🛒 Savat", callback_data="view_cart")
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_detail_keyboard(
    product_id: int,
    category_id: int,
    lang: str = "uz",
    cart_qty: int = 0
) -> InlineKeyboardMarkup:
    rows = []

    # Quantity controls or add to cart button
    if cart_qty > 0:
        rows.append([
            InlineKeyboardButton(text="➖", callback_data=f"cart_dec:{product_id}"),
            InlineKeyboardButton(text=f"🛒 Savatda: {cart_qty} dona", callback_data=f"view_cart"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_inc:{product_id}"),
        ])
    else:
        rows.append([
            InlineKeyboardButton(
                text=f"➕ {t('btn_add_to_cart', lang)}",
                callback_data=f"cart_add:{product_id}"
            )
        ])

    rows.append([
        InlineKeyboardButton(text="💬 Ushbu mahsulot haqida AI dan so'rash", callback_data=f"ai_ask_prod:{product_id}")
    ])
    rows.append([
        InlineKeyboardButton(text="⬅️ Ro'yxatga qaytish", callback_data=f"cat:{category_id}"),
        InlineKeyboardButton(text="🛒 Savat", callback_data="view_cart")
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cart_inline_keyboard(cart_items: List[CartItem], lang: str = "uz") -> InlineKeyboardMarkup:
    rows = []
    # Row for each item to adjust quantity
    for item in cart_items:
        pname = item.product.get_name(lang) if item.product else "Mahsulot"
        short_name = (pname[:16] + "..") if len(pname) > 18 else pname
        rows.append([
            InlineKeyboardButton(text=f"❌ {short_name}", callback_data=f"cart_del:{item.product_id}"),
            InlineKeyboardButton(text="➖", callback_data=f"cart_dec:{item.product_id}"),
            InlineKeyboardButton(text=f"{item.quantity} dona", callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_inc:{item.product_id}"),
        ])

    if cart_items:
        rows.append([
            InlineKeyboardButton(text=f"🚀 {t('btn_checkout', lang)}", callback_data="start_checkout")
        ])
        rows.append([
            InlineKeyboardButton(text=f"🗑 {t('btn_clear_cart', lang)}", callback_data="clear_cart"),
            InlineKeyboardButton(text="🛍 Katalogga qaytish", callback_data="back_categories")
        ])
    else:
        rows.append([
            InlineKeyboardButton(text="🛍 Xaridni boshlash", callback_data="back_categories")
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_panel_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦 Yangi buyurtmalar", callback_data="admin_orders:new"),
                InlineKeyboardButton(text="📊 Savdo statistikasi", callback_data="admin_stats"),
            ],
            [
                InlineKeyboardButton(text="➕ Yangi mahsulot qo'shish", callback_data="admin_add_product"),
                InlineKeyboardButton(text="📁 Kategoriyalar", callback_data="admin_categories"),
            ],
            [
                InlineKeyboardButton(text="🤖 AI sotuvchi yo'riqnomasini ko'rish/sozlash", callback_data="admin_ai_prompt"),
            ]
        ]
    )


def admin_order_actions_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"adm_status:{order_id}:accepted"),
                InlineKeyboardButton(text="🚚 Yetkazilmoqda", callback_data=f"adm_status:{order_id}:delivering"),
            ],
            [
                InlineKeyboardButton(text="🏁 Bajarildi", callback_data=f"adm_status:{order_id}:completed"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"adm_status:{order_id}:cancelled"),
            ],
            [
                InlineKeyboardButton(text="👤 Mijozga xabar yozish", callback_data=f"adm_msg_client:{order_id}")
            ]
        ]
    )
