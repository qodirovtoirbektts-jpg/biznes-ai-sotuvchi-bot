from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from bot.database.models import CartItem, Order, OrderItem, Product
from bot.utils.formatters import generate_order_number


class OrderService:
    @staticmethod
    async def create_order(
        session: AsyncSession,
        user_id: int,
        customer_name: str,
        customer_phone: str,
        delivery_address: str,
        latitude: Optional[float],
        longitude: Optional[float],
        payment_method: str,
        delivery_price: int = 20000,
        notes: Optional[str] = None
    ) -> Tuple[Optional[Order], str]:
        # Fetch cart
        stmt = select(CartItem).options(selectinload(CartItem.product)).where(CartItem.user_id == user_id)
        result = await session.execute(stmt)
        cart_items = list(result.scalars().all())

        if not cart_items:
            return None, "Savatingiz bo'sh!"

        # Calculate total
        subtotal = 0
        order_items_data = []

        for item in cart_items:
            prod = item.product
            if not prod or not prod.is_active:
                continue
            # check stock
            if prod.stock < item.quantity:
                return None, f"'{prod.name_uz}' mahsulotidan yetarli miqdorda qolmagan (qoldiq: {prod.stock})."

            item_total = prod.price * item.quantity
            subtotal += item_total
            order_items_data.append(
                OrderItem(
                    product_id=prod.id,
                    product_name=prod.name_uz,
                    price=prod.price,
                    quantity=item.quantity
                )
            )
            # decrement stock
            prod.stock -= item.quantity

        if not order_items_data:
            return None, "Savatdagi mahsulotlar mavjud emas."

        total_amount = subtotal + delivery_price
        order_number = generate_order_number()

        order = Order(
            order_number=order_number,
            user_id=user_id,
            total_amount=total_amount,
            delivery_price=delivery_price,
            status="new",
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            latitude=latitude,
            longitude=longitude,
            payment_method=payment_method,
            notes=notes,
            created_at=datetime.now(timezone.utc),
            items=order_items_data
        )

        session.add(order)

        # Clear cart
        for item in cart_items:
            await session.delete(item)

        await session.commit()
        await session.refresh(order)
        return order, "OK"

    @staticmethod
    async def get_user_orders(session: AsyncSession, user_id: int, limit: int = 10) -> List[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_order_by_id(session: AsyncSession, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items), selectinload(Order.user))
            .where(Order.id == order_id)
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_orders_by_status(session: AsyncSession, status: str, limit: int = 15) -> List[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.status == status)
            .order_by(Order.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update_order_status(session: AsyncSession, order_id: int, new_status: str) -> Optional[Order]:
        order = await OrderService.get_order_by_id(session, order_id)
        if not order:
            return None
        order.status = new_status
        await session.commit()
        return order

    @staticmethod
    async def get_statistics(session: AsyncSession) -> dict:
        total_orders_res = await session.execute(select(func.count(Order.id)))
        total_orders = total_orders_res.scalar() or 0

        total_rev_res = await session.execute(
            select(func.sum(Order.total_amount)).where(Order.status.in_(["accepted", "delivering", "completed"]))
        )
        total_revenue = total_rev_res.scalar() or 0

        # Today orders
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_orders_res = await session.execute(
            select(func.count(Order.id)).where(Order.created_at >= today_start)
        )
        today_orders = today_orders_res.scalar() or 0

        today_rev_res = await session.execute(
            select(func.sum(Order.total_amount))
            .where(Order.created_at >= today_start, Order.status.in_(["accepted", "delivering", "completed"]))
        )
        today_revenue = today_rev_res.scalar() or 0

        # Pending count
        pending_res = await session.execute(select(func.count(Order.id)).where(Order.status == "new"))
        pending_orders = pending_res.scalar() or 0

        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "today_orders": today_orders,
            "today_revenue": today_revenue,
            "pending_orders": pending_orders,
        }
