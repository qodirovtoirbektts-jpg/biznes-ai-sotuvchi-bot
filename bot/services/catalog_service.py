from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from bot.database.models import Category, Product


class CatalogService:
    @staticmethod
    async def get_categories(session: AsyncSession, only_active: bool = True) -> List[Category]:
        stmt = select(Category)
        if only_active:
            stmt = stmt.where(Category.is_active == True)  # noqa: E712
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_category(session: AsyncSession, category_id: int) -> Optional[Category]:
        return await session.get(Category, category_id)

    @staticmethod
    async def get_products_by_category(
        session: AsyncSession,
        category_id: int,
        only_active: bool = True
    ) -> List[Product]:
        stmt = select(Product).where(Product.category_id == category_id)
        if only_active:
            stmt = stmt.where(Product.is_active == True)  # noqa: E712
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_product(session: AsyncSession, product_id: int) -> Optional[Product]:
        stmt = select(Product).options(selectinload(Product.category)).where(Product.id == product_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def search_products(session: AsyncSession, query: str, limit: int = 10) -> List[Product]:
        search_pattern = f"%{query}%"
        stmt = (
            select(Product)
            .where(
                Product.is_active == True,  # noqa: E712
                (
                    Product.name_uz.ilike(search_pattern)
                    | Product.name_ru.ilike(search_pattern)
                    | Product.description.ilike(search_pattern)
                )
            )
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_all_active_products_summary(session: AsyncSession) -> List[dict]:
        stmt = select(Product).options(selectinload(Product.category)).where(Product.is_active == True)  # noqa: E712
        result = await session.execute(stmt)
        products = result.scalars().all()
        summary = []
        for p in products:
            summary.append({
                "id": p.id,
                "name": p.name_uz,
                "category": p.category.name_uz if p.category else "",
                "price": p.price,
                "stock": p.stock,
                "description": p.description or ""
            })
        return summary
