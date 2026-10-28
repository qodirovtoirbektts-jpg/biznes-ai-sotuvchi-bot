import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.database.base import Base
from bot.database.models import User, Category, Product, CartItem, Order, OrderItem


@pytest.fixture
async def async_session():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await test_engine.dispose()


@pytest.mark.asyncio
async def test_create_user_and_product(async_session: AsyncSession):
    user = User(id=12345, full_name="Ali Valiyev", language_code="uz", is_admin=False)
    async_session.add(user)

    cat = Category(name_uz="Smartfonlar", name_ru="Смартфоны")
    async_session.add(cat)
    await async_session.flush()

    prod = Product(
        category_id=cat.id,
        name_uz="iPhone 15",
        name_ru="iPhone 15",
        price=12000000,
        stock=10
    )
    async_session.add(prod)
    await async_session.commit()

    assert user.id == 12345
    assert prod.id is not None
    assert prod.price == 12000000
    assert cat.get_name("ru") == "Смартфоны"
    assert cat.get_name("uz") == "Smartfonlar"
