from typing import Dict, Any

MESSAGES: Dict[str, Dict[str, str]] = {
    "welcome": {
        "uz": (
            "Assalomu alaykum, {name}! 👋\n\n"
            "**\"{store_name}\"** savdo botiga xush kelibsiz!\n"
            "Men sizning shaxsiy **AI Sotuvchi Maslahatchingizman**.\n\n"
            "✨ Sizga mahsulot tanlashda, savollarga javob berishda va tezkor buyurtma rasmiylashtirishda yordam beraman.\n\n"
            "Quyidagi tugmalardan birini tanlang yoki to'g'ridan-to'g'ri menga savolingizni yozing / ovozli xabar yuboring:"
        ),
        "oz": (
            "Ассалому алайкум, {name}! 👋\n\n"
            "**\"{store_name}\"** савдо ботига хуш келибсиз!\n"
            "Мен сизнинг шахсий **AI Сотувчи Маслаҳатчингизман**.\n\n"
            "✨ Сизга маҳсулот танлашда, саволларга жавоб беришда ва тезкор буюртма расмийлаштиришда ёрдам бераман.\n\n"
            "Қуйидаги тугмалардан бирини танланг ёки тўғридан-тўғри менга саволингизни ёзинг / овозли хабар юборинг:"
        ),
        "ru": (
            "Здравствуйте, {name}! 👋\n\n"
            "Добро пожаловать в бот **\"{store_name}\"**!\n"
            "Я ваш персональный **AI Продавец-Консультант**.\n\n"
            "✨ Я помогу вам подобрать товар, отвечу на любые вопросы и быстро оформлю заказ.\n\n"
            "Выберите раздел ниже или просто напишите мне / отправьте голосовое сообщение:"
        ),
    },
    "choose_language": {
        "uz": "🌐 Iltimos, tilni tanlang:",
        "oz": "🌐 Илтимос, тилни танланг:",
        "ru": "🌐 Пожалуйста, выберите язык:",
    },
    "lang_changed": {
        "uz": "✅ Til muvaffaqiyatli o'zgartirildi: O'zbekcha 🇺🇿",
        "oz": "✅ Тил муваффақиятли ўзгартирилди: Ўзбекча 🇺🇿",
        "ru": "✅ Язык успешно изменен: Русский 🇷🇺",
    },
    "btn_catalog": {
        "uz": "🛍 Mahsulotlar katalogi",
        "oz": "🛍 Маҳсулотлар каталоги",
        "ru": "🛍 Каталог товаров",
    },
    "btn_cart": {
        "uz": "🛒 Savat",
        "oz": "🛒 Сават",
        "ru": "🛒 Корзина",
    },
    "btn_orders": {
        "uz": "📦 Buyurtmalarim",
        "oz": "📦 Буюртмаларим",
        "ru": "📦 Мои заказы",
    },
    "btn_ai_sales": {
        "uz": "💬 AI Maslahatchi",
        "oz": "💬 AI Маслаҳатчи",
        "ru": "💬 AI Консультант",
    },
    "btn_about": {
        "uz": "ℹ️ Do'kon haqida",
        "oz": "ℹ️ Дўкон ҳақида",
        "ru": "ℹ️ О магазине",
    },
    "btn_contact": {
        "uz": "📞 Bog'lanish",
        "oz": "📞 Боғланиш",
        "ru": "📞 Контакты",
    },
    "btn_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "oz": "🌐 Тилни ўзгартириш",
        "ru": "🌐 Сменить язык",
    },
    "btn_admin_panel": {
        "uz": "⚙️ Admin Panel",
        "oz": "⚙️ Админ Панел",
        "ru": "⚙️ Админ Панель",
    },
    "categories_title": {
        "uz": "📂 **Mahsulot kategoriyalari:**\nQiziqtirgan bo'limni tanlang:",
        "oz": "📂 **Маҳсулот категориялари:**\nҚизиқтирган бўлимни танланг:",
        "ru": "📂 **Категории товаров:**\nВыберите интересующую категорию:",
    },
    "products_in_category": {
        "uz": "📦 **{category}** bo'limidagi mahsulotlar:",
        "oz": "📦 **{category}** бўлимидаги маҳсулотлар:",
        "ru": "📦 Товары в категории **{category}**:",
    },
    "empty_category": {
        "uz": "Ushbu bo'limda hozircha mahsulotlar mavjud emas.",
        "oz": "Ушбу бўлимда ҳозирча маҳсулотлар мавжуд эмас.",
        "ru": "В этой категории пока нет товаров.",
    },
    "product_details": {
        "uz": (
            "🏷 **{name}**\n\n"
            "📝 **Tavsif:**\n{description}\n\n"
            "💰 **Narxi:** {price} so'm\n"
            "📦 **Mavjudligi:** {stock} dona"
        ),
        "oz": (
            "🏷 **{name}**\n\n"
            "📝 **Тавсиф:**\n{description}\n\n"
            "💰 **Нархи:** {price} сўм\n"
            "📦 **Мавжудлиги:** {stock} дона"
        ),
        "ru": (
            "🏷 **{name}**\n\n"
            "📝 **Описание:**\n{description}\n\n"
            "💰 **Цена:** {price} сум\n"
            "📦 **В наличии:** {stock} шт."
        ),
    },
    "added_to_cart": {
        "uz": "✅ **\"{product_name}\"** savatga qo'shildi!",
        "oz": "✅ **\"{product_name}\"** саватга қўшилди!",
        "ru": "✅ **\"{product_name}\"** добавлен в корзину!",
    },
    "cart_empty": {
        "uz": "🛒 Savatingiz bo'sh.\nMahsulotlar katalogidan o'zingizga yoqqan tovarlarni tanlang!",
        "oz": "🛒 Саватингиз бўш.\nМаҳсулотлар каталогидан ўзингизга ёққан товарларни танланг!",
        "ru": "🛒 Ваша корзина пуста.\nВыберите понравившиеся товары в каталоге!",
    },
    "cart_title": {
        "uz": "🛒 **Sizning savatingiz:**\n\n{items}\n\n🏷 **Mahsulotlar:** {subtotal} so'm\n🚚 **Yetkazib berish:** {delivery} so'm\n💰 **Jami to'lov:** {total} so'm",
        "oz": "🛒 **Сизнинг саватингиз:**\n\n{items}\n\n🏷 **Маҳсулотлар:** {subtotal} сўм\n🚚 **Етказиб бериш:** {delivery} сўм\n💰 **Жами тўлов:** {total} сўм",
        "ru": "🛒 **Ваша корзина:**\n\n{items}\n\n🏷 **Товары:** {subtotal} сум\n🚚 **Доставка:** {delivery} сум\n💰 **Итого к оплате:** {total} сум",
    },
    "checkout_start_name": {
        "uz": "👤 Buyurtmani rasmiylashtirish uchun ismingizni kiriting:",
        "oz": "👤 Буюртмани расмийлаштириш учун исмингизни киритинг:",
        "ru": "👤 Для оформления заказа введите ваше имя:",
    },
    "checkout_ask_phone": {
        "uz": "📞 Aloqa uchun telefon raqamingizni kiriting yoki quyidagi tugma orqali yuboring:",
        "oz": "📞 Алоқа учун телефон рақамингизни киритинг ёки қуйидаги тугма орқали юборинг:",
        "ru": "📞 Введите номер телефона для связи или отправьте по кнопке ниже:",
    },
    "checkout_ask_location": {
        "uz": "📍 Yetkazib berish manzilini yozing yoki geolokatsiyangizni yuboring:",
        "oz": "📍 Етказиб бериш манзилини ёзинг ёки геолокациянгизни юборинг:",
        "ru": "📍 Введите адрес доставки или отправьте геолокацию:",
    },
    "checkout_ask_payment": {
        "uz": "💳 To'lov turini tanlang:",
        "oz": "💳 Тўлов турини танланг:",
        "ru": "💳 Выберите способ оплаты:",
    },
    "order_confirmed": {
        "uz": (
            "🎉 **Buyurtmangiz qabul qilindi!**\n\n"
            "🆔 **Buyurtma raqami:** #{order_number}\n"
            "💰 **Umumiy summa:** {total} so'm\n"
            "📞 **Telefon:** {phone}\n"
            "📍 **Manzil:** {address}\n"
            "💳 **To'lov turi:** {payment}\n\n"
            "Tez orada menejerimiz siz bilan bog'lanadi. Buyurtma holatini \"📦 Buyurtmalarim\" bo'limida kuzatishingiz mumkin!"
        ),
        "oz": (
            "🎉 **Буюртмангиз қабул қилинди!**\n\n"
            "🆔 **Буюртма рақами:** #{order_number}\n"
            "💰 **Умумий сумма:** {total} сўм\n"
            "📞 **Телефон:** {phone}\n"
            "📍 **Манзил:** {address}\n"
            "💳 **Тўлов тури:** {payment}\n\n"
            "Тез орада менежеримиз сиз билан боғланади. Буюртма ҳолатини \"📦 Буюртмаларим\" бўлимида кузатишингиз мумкин!"
        ),
        "ru": (
            "🎉 **Ваш заказ успешно оформлен!**\n\n"
            "🆔 **Номер заказа:** #{order_number}\n"
            "💰 **Итоговая сумма:** {total} сум\n"
            "📞 **Телефон:** {phone}\n"
            "📍 **Адрес:** {address}\n"
            "💳 **Способ оплаты:** {payment}\n\n"
            "Наш менеджер свяжется с вами в ближайшее время. Отслеживать заказ можно в разделе \"📦 Мои заказы\"!"
        ),
    },
    "status_updated_notify": {
        "uz": "🔔 **Buyurtma holati yangilandi!**\n\n🆔 Buyurtma #{order_number}\nHolat: **{status}**",
        "oz": "🔔 **Буюртма ҳолати янгиланди!**\n\n🆔 Буюртма #{order_number}\nҲолат: **{status}**",
        "ru": "🔔 **Статус заказа обновлен!**\n\n🆔 Заказ #{order_number}\nСтатус: **{status}**",
    },
    "ai_consultant_intro": {
        "uz": (
            "🤖 **Men sizning AI Sotuvchi Maslahatchingizman!**\n\n"
            "Siz menga xohlagan mahsulot haqida yozishingiz yoki ovozli xabar yuborishingiz mumkin. "
            "Masalan:\n"
            "• *\"Menga 15 milliongacha sovg'a uchun telefon tavsiya qiling\"*\n"
            "• *\"O'yinlar uchun noutbuk bormi?\"*\n"
            "• *\"AirPods Pro 2 ning qanday ustunliklari bor?\"*\n\n"
            "Savolingizni yozing yoki ovoz yuboring:"
        ),
        "oz": (
            "🤖 **Мен сизнинг AI Сотувчи Маслаҳатчингизман!**\n\n"
            "Сиз менга хоҳлаган маҳсулот ҳақида ёзишингиз ёки овозли хабар юборишингиз мумкин. "
            "Масалан:\n"
            "• *\"Менга 15 миллионгача совға учун телефон тавсия қилинг\"*\n"
            "• *\"Ўйинлар учун ноутбук борми?\"*\n"
            "• *\"AirPods Pro 2 нинг қандай устунликлари бор?\"*\n\n"
            "Саволингизни ёзинг ёки овоз юборинг:"
        ),
        "ru": (
            "🤖 **Я ваш AI Продавец-Консультант!**\n\n"
            "Вы можете задать любой вопрос о товарах текстом или голосовым сообщением. "
            "Например:\n"
            "• *\"Посоветуйте смартфон до 15 млн сум на подарок\"*\n"
            "• *\"Есть мощный ноутбук для игр?\"*\n"
            "• *\"В чем преимущества AirPods Pro 2?\"*\n\n"
            "Напишите ваш вопрос или отправьте голосовое сообщение:"
        ),
    },
    "about_text": {
        "uz": (
            "🏪 **\"{store_name}\"**\n\n"
            "📝 {store_description}\n\n"
            "📍 Yetkazib berish xizmati: Butun respublika bo'ylab mavjud.\n"
            "⏱ Ish vaqti: 24/7 (AI maslahatchi har doim xizmatingizda)\n"
            "📞 Telefon: {store_phone}\n\n"
            "Biz har bir mijozimizga yuqori sifat va tezkor xizmat ko'rsatishdan mamnunmiz!"
        ),
        "oz": (
            "🏪 **\"{store_name}\"**\n\n"
            "📝 {store_description}\n\n"
            "📍 Етказиб бериш хизмати: Бутун республика бўйлаб мавжуд.\n"
            "⏱ Иш вақти: 24/7 (AI маслаҳатчи ҳар доим хизматингизда)\n"
            "📞 Телефон: {store_phone}\n\n"
            "Биз ҳар бир мижозимизга юқори сифат ва тезкор хизмат кўрсатишдан мамнунмиз!"
        ),
        "ru": (
            "🏪 **\"{store_name}\"**\n\n"
            "📝 {store_description}\n\n"
            "📍 Служба доставки: По всей республике.\n"
            "⏱ График работы: 24/7 (AI консультант на связи всегда)\n"
            "📞 Телефон: {store_phone}\n\n"
            "Мы гарантируем оригинальное качество и быструю доставку каждого заказа!"
        ),
    },
    "contact_text": {
        "uz": "📞 **Biz bilan bog'lanish:**\n\nTelefon: {phone}\nSavollar yoki takliflar bo'lsa, xodimlarimiz doimo javob berishga tayyor!",
        "oz": "📞 **Биз билан боғланиш:**\n\nТелефон: {phone}\nСаволлар ёки таклифлар бўлса, ходимларимиз доимо жавоб беришга тайёр!",
        "ru": "📞 **Контакты:**\n\nТелефон: {phone}\nПо всем вопросам наши операторы всегда готовы вам помочь!",
    },
    "btn_back": {
        "uz": "⬅️ Orqaga",
        "oz": "⬅️ Орқага",
        "ru": "⬅️ Назад",
    },
    "btn_main_menu": {
        "uz": "🏠 Asosiy menyu",
        "oz": "🏠 Асосий меню",
        "ru": "🏠 Главное меню",
    },
    "btn_add_to_cart": {
        "uz": "🛒 Savatga qo'shish",
        "oz": "🛒 Саватга қўшиш",
        "ru": "🛒 В корзину",
    },
    "btn_checkout": {
        "uz": "✅ Buyurtma berish",
        "oz": "✅ Оформить заказ",
        "ru": "✅ Оформить заказ",
    },
    "btn_clear_cart": {
        "uz": "🗑 Savatni tozalash",
        "oz": "🗑 Саватни тозалаш",
        "ru": "🗑 Очистить корзину",
    },
    "btn_send_contact": {
        "uz": "📱 Telefon raqamni yuborish",
        "oz": "📱 Телефон рақамни юбориш",
        "ru": "📱 Поделиться контактом",
    },
    "btn_send_location": {
        "uz": "📍 Lokatsiyani yuborish",
        "oz": "📍 Локацияни юбориш",
        "ru": "📍 Отправить локацию",
    },
    "btn_cancel": {
        "uz": "❌ Bekor qilish",
        "oz": "❌ Бекор қилиш",
        "ru": "❌ Отмена",
    },
    "order_cancelled": {
        "uz": "Jarayon bekor qilindi.",
        "oz": "Жараён бекор қилинди.",
        "ru": "Действие отменено.",
    },
    "payment_cash": {
        "uz": "💵 Naqd pul (qabul qilinganda)",
        "oz": "💵 Нақд пул (қабул қилинганда)",
        "ru": "💵 Наличными при получении",
    },
    "payment_click": {
        "uz": "💳 Click orqali",
        "oz": "💳 Click орқали",
        "ru": "💳 Через Click",
    },
    "payment_payme": {
        "uz": "💳 Payme orqali",
        "oz": "💳 Payme орқали",
        "ru": "💳 Через Payme",
    },
}

STATUS_NAMES: Dict[str, Dict[str, str]] = {
    "new": {
        "uz": "🆕 Yangi (qabul qilinmoqda)",
        "oz": "🆕 Янги (қабул қилинмоқда)",
        "ru": "🆕 Новый (в обработке)",
    },
    "accepted": {
        "uz": "✅ Qabul qilindi (tayyorlanmoqda)",
        "oz": "✅ Қабул қилинди (тайёрланмоқда)",
        "ru": "✅ Принят (готовится)",
    },
    "delivering": {
        "uz": "🚚 Yetkazilmoqda (kuryer yo'lda)",
        "oz": "🚚 Етказилмоқда (курьер йўлда)",
        "ru": "🚚 В пути (курьер доставляет)",
    },
    "completed": {
        "uz": "🏁 Yetkazib berildi (yakunlandi)",
        "oz": "🏁 Етказиб берилди (якунланди)",
        "ru": "🏁 Доставлен (завершен)",
    },
    "cancelled": {
        "uz": "❌ Bekor qilingan",
        "oz": "❌ Бекор қилинган",
        "ru": "❌ Отменен",
    },
}


def t(key: str, lang: str = "uz", **kwargs: Any) -> str:
    lang = lang if lang in ("uz", "oz", "ru") else "uz"
    template = MESSAGES.get(key, {}).get(lang) or MESSAGES.get(key, {}).get("uz", key)
    try:
        return template.format(**kwargs)
    except Exception:
        return template


def get_status_label(status: str, lang: str = "uz") -> str:
    lang = lang if lang in ("uz", "oz", "ru") else "uz"
    return STATUS_NAMES.get(status, {}).get(lang, status)
