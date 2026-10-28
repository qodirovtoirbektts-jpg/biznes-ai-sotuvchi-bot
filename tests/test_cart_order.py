import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.database.base import Base
from bot.database.models import User, Category, Product
from bot.services.cart_service import CartService
from bot.services.order_service import OrderService


@pytest.fixture
async def db_session():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await test_engine.dispose()


@pytest.mark.asyncio
async def test_cart_operations_and_order_flow(db_session: AsyncSession):
    user = User(id=999, full_name="Test Xaridor", language_code="uz")
    db_session.add(user)

    cat = Category(name_uz="Aksessuarlar")
    db_session.add(cat)
    await db_session.flush()

    prod = Product(
        category_id=cat.id,
        name_uz="Powerbank 20000mAh",
        price=500000,
        stock=10
    )
    db_session.add(prod)
    await db_session.commit()

    # 1. Add to cart
    await CartService.add_to_cart(db_session, user_id=999, product_id=prod.id, quantity=2)
    cart_items = await CartService.get_cart(db_session, user_id=999)
    assert len(cart_items) == 1
    assert cart_items[0].quantity == 2

    # 2. Calculate totals
    subtotal, delivery, total = CartService.calculate_totals(cart_items, delivery_price=20000)
    assert subtotal == 1000000
    assert delivery == 20000
    assert total == 1020000

    # 3. Create Order
    order, status_msg = await OrderService.create_order(
        session=db_session,
        user_id=999,
        customer_name="Test Xaridor",
        customer_phone="+998901112233",
        delivery_address="Toshkent, Amir Temur 1",
        latitude=41.31,
        longitude=69.24,
        payment_method="cash",
        delivery_price=20000
    )

    assert status_msg == "OK"
    assert order is not None
    assert order.total_amount == 1020000
    assert order.status == "new"
    assert len(order.items) == 1

    # Check stock decreased from 10 to 8
    await db_session.refresh(prod)
    assert prod.stock == 8

    # Check cart is cleared
    cart_after = await CartService.get_cart(db_session, user_id=999)
    assert len(cart_after) == 0

    # 4. Status update
    updated = await OrderService.update_order_status(db_session, order.id, "accepted")
    assert updated.status == "accepted"
