from typing import List, Optional, Tuple
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from bot.database.models import CartItem, Product


class CartService:
    @staticmethod
    async def get_cart(session: AsyncSession, user_id: int) -> List[CartItem]:
        stmt = (
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_item_quantity(session: AsyncSession, user_id: int, product_id: int) -> int:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await session.execute(stmt)
        item = result.scalars().first()
        return item.quantity if item else 0

    @staticmethod
    async def add_to_cart(
        session: AsyncSession,
        user_id: int,
        product_id: int,
        quantity: int = 1
    ) -> CartItem:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await session.execute(stmt)
        item = result.scalars().first()

        if item:
            item.quantity += quantity
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(item)

        await session.commit()
        return item

    @staticmethod
    async def update_quantity(
        session: AsyncSession,
        user_id: int,
        product_id: int,
        delta: int
    ) -> Optional[int]:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await session.execute(stmt)
        item = result.scalars().first()
        if not item:
            return 0

        new_qty = item.quantity + delta
        if new_qty <= 0:
            await session.delete(item)
            await session.commit()
            return 0

        item.quantity = new_qty
        await session.commit()
        return new_qty

    @staticmethod
    async def remove_item(session: AsyncSession, user_id: int, product_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def clear_cart(session: AsyncSession, user_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.user_id == user_id)
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    def calculate_totals(
        cart_items: List[CartItem],
        delivery_price: int = 20000
    ) -> Tuple[int, int, int]:
        """Returns (subtotal, delivery_price, total_amount)."""
        subtotal = sum(
            (item.product.price if item.product else 0) * item.quantity
            for item in cart_items
        )
        if subtotal == 0:
            return (0, 0, 0)
        total = subtotal + delivery_price
        return (subtotal, delivery_price, total)
