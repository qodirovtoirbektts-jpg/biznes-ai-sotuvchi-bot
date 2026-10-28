import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import Category, Product, StoreSetting
from bot.config import settings

logger = logging.getLogger(__name__)


async def seed_initial_data(session: AsyncSession) -> None:
    # Check if categories already exist
    result = await session.execute(select(Category))
    if result.scalars().first() is not None:
        return

    logger.info("Database is empty. Populating initial seed data...")

    # Default categories and products
    cat_gadgets = Category(
        name_uz="Smartfonlar va Gadjetlar",
        name_oz="Смартфонлар ва Гаджетлар",
        name_ru="Смартфоны и Гаджеты",
        description="Eng so'nggi rusumdagi smartfonlar va quloqchinlar"
    )
    cat_laptops = Category(
        name_uz="Noutbuklar va Kompyuterlar",
        name_oz="Ноутбуклар ва Компьютерлар",
        name_ru="Ноутбуки и Компьютеры",
        description="Ish va o'yinlar uchun kuchli noutbuklar"
    )
    cat_accessories = Category(
        name_uz="Aksessuarlar va Powerbanklar",
        name_oz="Акссессуарлар ва Пауэрбанклар",
        name_ru="Аксессуары и Пауэрбанки",
        description="Sifatli zaryadlovchilar va kabellar"
    )
    cat_lifestyle = Category(
        name_uz="Kiyim va Poyabzallar",
        name_oz="Кийим ва Поябзаллар",
        name_ru="Одежда и Обувь",
        description="Qulay va zamonaviy kundalik kiyimlar"
    )

    session.add_all([cat_gadgets, cat_laptops, cat_accessories, cat_lifestyle])
    await session.flush()

    products = [
        Product(
            category_id=cat_gadgets.id,
            name_uz="iPhone 15 Pro Max 256GB Natural Titanium",
            name_oz="iPhone 15 Pro Max 256GB Natural Titanium",
            name_ru="iPhone 15 Pro Max 256GB Natural Titanium",
            description="Titan korpus, A17 Pro kuchli protsessor, 5x optik zoom va ajoyib akkumulyator quvvati. 1 yil rasmiy kafolat.",
            price=15200000,
            stock=15,
            image_url="https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800"
        ),
        Product(
            category_id=cat_gadgets.id,
            name_uz="Samsung Galaxy S24 Ultra 12/256GB Gray",
            name_oz="Samsung Galaxy S24 Ultra 12/256GB Gray",
            name_ru="Samsung Galaxy S24 Ultra 12/256GB Gray",
            description="Galaxy AI imkoniyatlari, o'rnatilgan S-Pen qalami, 200MP kamera va yorqin Dynamic AMOLED ekran.",
            price=14500000,
            stock=12,
            image_url="https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800"
        ),
        Product(
            category_id=cat_gadgets.id,
            name_uz="Apple AirPods Pro 2 (USB-C MagSafe)",
            name_oz="Apple AirPods Pro 2 (USB-C MagSafe)",
            name_ru="Apple AirPods Pro 2 (USB-C MagSafe)",
            description="Faol shovqinni bekor qilish (ANC), shaffof rejim va fazoviy audio qo'llab-quvvatlovi.",
            price=2750000,
            stock=30,
            image_url="https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800"
        ),
        Product(
            category_id=cat_laptops.id,
            name_uz="MacBook Air 15 M3 16GB / 512GB Midnight",
            name_oz="MacBook Air 15 M3 16GB / 512GB Midnight",
            name_ru="MacBook Air 15 M3 16GB / 512GB Midnight",
            description="Yangi Apple M3 chipi, 18 soatgacha batareya muddati, jim va yupqa alyuminiy korpus.",
            price=18900000,
            stock=8,
            image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800"
        ),
        Product(
            category_id=cat_laptops.id,
            name_uz="ASUS ROG Zephyrus G16 (RTX 4070 / i9 / 32GB)",
            name_oz="ASUS ROG Zephyrus G16 (RTX 4070 / i9 / 32GB)",
            name_ru="ASUS ROG Zephyrus G16 (RTX 4070 / i9 / 32GB)",
            description="240Hz OLED ekran, ultra yupqa dizayn, og'ir o'yinlar va grafika uchun ideal quvvat.",
            price=24500000,
            stock=5,
            image_url="https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800"
        ),
        Product(
            category_id=cat_accessories.id,
            name_uz="Anker 735 GaNPrime 65W Zaryadlovchi Blok",
            name_oz="Anker 735 GaNPrime 65W Зарядловчи Блок",
            name_ru="Сетевое зарядное устройство Anker 735 GaNPrime 65W",
            description="3 ta port (2x Type-C, 1x USB-A). Telefon, planshet va noutbukni bir vaqtning o'zida tez quvvatlaydi.",
            price=460000,
            stock=45,
            image_url="https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800"
        ),
        Product(
            category_id=cat_accessories.id,
            name_uz="Baseus Blade 100W 20000mAh Power Bank",
            name_oz="Baseus Blade 100W 20000mAh Power Bank",
            name_ru="Внешний аккумулятор Baseus Blade 100W 20000mAh",
            description="Yupqa dizayn, raqamli displey, noutbuklarni ham to'liq quvvatlay oluvchi 100W quvvat.",
            price=590000,
            stock=25,
            image_url="https://images.unsplash.com/photo-1609592424109-dd9892f1b177?w=800"
        ),
        Product(
            category_id=cat_lifestyle.id,
            name_uz="Nike Air Force 1 '07 Classic White",
            name_oz="Nike Air Force 1 '07 Classic White",
            name_ru="Кроссовки Nike Air Force 1 '07 Classic White",
            description="Klassik afsonaviy oq krossovka, tabiiy charm va uzoq yillik qulaylik.",
            price=1250000,
            stock=20,
            image_url="https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800"
        ),
    ]

    session.add_all(products)

    settings_data = [
        StoreSetting(key="store_name", value=settings.STORE_NAME),
        StoreSetting(key="store_description", value=settings.STORE_DESCRIPTION),
        StoreSetting(key="store_phone", value=settings.STORE_PHONE),
        StoreSetting(
            key="ai_system_prompt",
            value=(
                "Siz 'Biznes AI Sotuvchi' do'koni uchun eng mahoratli, xushmuomala va sotuv natijalariga yo'naltirilgan AI sotuvchi-maslahatchisiz. "
                "Vazifangiz: Mijoz ehtiyojini aniqlash, do'konda mavjud tovarlardan eng mosini tavsiya qilish, "
                "narx va xususiyatlarini tushuntirish hamda savatga qo'shib buyurtma berishga taklif qilish. "
                "Mijoz qaysi tilda yozsa (o'zbekcha lotin, kirill yoki ruscha), aynan o'sha tilda javob bering."
            )
        )
    ]
    session.add_all(settings_data)

    await session.commit()
    logger.info("Seed data successfully populated.")
