import random
from datetime import datetime, timezone
from typing import List
from bot.database.models import CartItem, Order, OrderItem
from bot.utils.i18n import get_status_label


def format_currency(amount: int) -> str:
    """Format integer amount to readable spaced currency string, e.g. 15 200 000."""
    return f"{amount:,}".replace(",", " ")


def generate_order_number() -> str:
    """Generate unique human readable order number."""
    now = datetime.now(timezone.utc)
    rand_suffix = random.randint(1000, 9999)
    return f"{now.strftime('%y%m%d')}-{rand_suffix}"


def format_cart_items_text(cart_items: List[CartItem], lang: str = "uz") -> str:
    """Build readable bullet list of cart items."""
    if not cart_items:
        return ""
    lines = []
    for idx, item in enumerate(cart_items, 1):
        pname = item.product.get_name(lang) if item.product else "Mahsulot"
        item_total = (item.product.price if item.product else 0) * item.quantity
        lines.append(
            f"{idx}. **{pname}**\n"
            f"   {item.quantity} x {format_currency(item.product.price if item.product else 0)} = **{format_currency(item_total)} so'm**"
        )
    return "\n".join(lines)


def format_order_summary(order: Order, lang: str = "uz") -> str:
    """Format single order details for customer view."""
    items_text = []
    for idx, item in enumerate(order.items, 1):
        sub = item.price * item.quantity
        items_text.append(f"{idx}. {item.product_name} — {item.quantity} x {format_currency(item.price)} = {format_currency(sub)} so'm")

    status_str = get_status_label(order.status, lang)
    date_str = order.created_at.strftime("%Y-%m-%d %H:%M")

    payment_labels = {
        "cash": "💵 Naqd pul",
        "click": "💳 Click",
        "payme": "💳 Payme"
    }
    pay_str = payment_labels.get(order.payment_method, order.payment_method)

    text = (
        f"📦 **Buyurtma #{order.order_number}**\n"
        f"📅 Sana: {date_str}\n"
        f"📊 Holat: **{status_str}**\n"
        f"💳 To'lov: {pay_str}\n\n"
        f"📝 **Tarkib:**\n" + ("\n".join(items_text) or "Mahsulotlar") + "\n\n"
        f"🚚 Yetkazib berish: {format_currency(order.delivery_price)} so'm\n"
        f"💰 **Jami:** {format_currency(order.total_amount)} so'm\n"
        f"📍 Manzil: {order.delivery_address or 'Ko\'rsatilmagan'}"
    )
    return text


def format_admin_order_notification(order: Order) -> str:
    """Format comprehensive order alert for store administrators."""
    items_text = []
    for idx, item in enumerate(order.items, 1):
        sub = item.price * item.quantity
        items_text.append(f"  {idx}. {item.product_name} ({item.quantity} dona) — {format_currency(sub)} so'm")

    status_str = get_status_label(order.status, "uz")
    pay_map = {"cash": "Naqd", "click": "Click", "payme": "Payme"}

    msg = (
        f"🚨 **YANGI BUYURTMA #{order.order_number}** 🚨\n\n"
        f"👤 **Xaridor:** {order.customer_name}\n"
        f"📞 **Telefon:** `{order.customer_phone}`\n"
        f"🆔 **Telegram ID:** `{order.user_id}`\n"
        f"📍 **Manzil:** {order.delivery_address or 'Ko\'rsatilmagan'}\n"
        f"💳 **To'lov turi:** {pay_map.get(order.payment_method, order.payment_method)}\n"
        f"📊 **Holati:** {status_str}\n\n"
        f"🛒 **Buyurtma tarkibi:**\n" + "\n".join(items_text) + "\n\n"
        f"🚚 Yetkazib berish: {format_currency(order.delivery_price)} so'm\n"
        f"💰 **JAMI SUMMA:** **{format_currency(order.total_amount)} so'm**\n"
    )
    if order.notes:
        msg += f"\n💬 Izoh: {order.notes}"
    return msg
