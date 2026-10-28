import json
import logging
import re
import warnings
from typing import Any, Dict, List, Optional, Tuple

warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import settings
from bot.services.catalog_service import CatalogService
from bot.utils.formatters import format_currency

logger = logging.getLogger(__name__)


class GeminiSalesService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
        self._configured = False
        if self.api_key and self.api_key.strip():
            try:
                genai.configure(api_key=self.api_key.strip())
                self._configured = True
            except Exception as e:
                logger.error(f"Error configuring Gemini API: {e}")

    async def generate_sales_response(
        self,
        session: AsyncSession,
        user_message: str,
        user_lang: str = "uz",
        history: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[str, List[int]]:
        """
        Process user question/inquiry and generate an AI consultative sales response.
        Returns (response_text, recommended_product_ids).
        """
        products = await CatalogService.get_all_active_products_summary(session)

        # Check if configured
        if not self._configured or not self.api_key:
            return self._fallback_sales_engine(user_message, products, user_lang)

        try:
            # Build catalog context
            catalog_lines = []
            for p in products:
                catalog_lines.append(
                    f"- ID: {p['id']} | Nomi: {p['name']} | Kategoriya: {p['category']} | "
                    f"Narxi: {format_currency(p['price'])} so'm | Qoldiq: {p['stock']} dona | "
                    f"Tavsif: {p['description']}"
                )
            catalog_str = "\n".join(catalog_lines)

            system_instruction = (
                f"Siz '{settings.STORE_NAME}' do'konining professional, samimiy va tajribali "
                f"AI Sotuvchi Maslahatchisisiz (Sales Consultant).\n"
                f"Do'kon tavsifi: {settings.STORE_DESCRIPTION}\n"
                f"Telefon: {settings.STORE_PHONE}\n"
                f"Yetkazib berish narxi: {format_currency(settings.DELIVERY_PRICE)} so'm (respublika bo'ylab mavjud).\n\n"
                f"DO'KONDA MAVJUD MAHSULOTLAR RO'YXATI:\n{catalog_str}\n\n"
                f"KO'RSATMALAR:\n"
                f"1. Mijozning savolini diqqat bilan tahlil qiling. Agar u ma'lum bir mahsulot, narx yoki tavsiya so'rayotgan bo'lsa, "
                f"mavjud ro'yxatdan eng munosiblarini aniq va qiziqarli qilib tushuntirib bering.\n"
                f"2. Savdo mahoratini (sales pitch) qo'llang: mahsulotning asosiy afzalliklarini ayting, xushmuomala bo'ling "
                f"va javob oxirida savatga qo'shish yoki buyurtma berishni taklif qiling.\n"
                f"3. Mijoz qaysi tilda murojaat qilgan bo'lsa (o'zbekcha lotin, kirill yoki ruscha), aynan o'sha tilda javob bering.\n"
                f"4. Javobingiz oxirida, agar mijozga ma'lum mahsulotlarni tavsiya qilgan bo'lsangiz, maxsus tegga ularning ID larini kiriting:\n"
                f"Masalan: [RECOMMENDED_IDS: 1, 3]\n"
                f"Agar hech qanday aniq mahsulot tavsiya qilinmagan bo'lsa: [RECOMMENDED_IDS:]\n"
                f"Ushbu teg bot tugmalarini chiqarish uchun kerak."
            )

            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )

            prompt = f"Mijoz savoli: {user_message}"
            response = await model.generate_content_async(prompt)
            raw_text = response.text or ""

            # Extract recommended IDs
            rec_ids = []
            rec_match = re.search(r"\[RECOMMENDED_IDS:\s*([\d,\s]*)\]", raw_text)
            clean_text = raw_text
            if rec_match:
                ids_str = rec_match.group(1).strip()
                if ids_str:
                    rec_ids = [int(x.strip()) for x in ids_str.split(",") if x.strip().isdigit()]
                clean_text = re.sub(r"\[RECOMMENDED_IDS:\s*[\d,\s]*\]", "", raw_text).strip()

            return clean_text, rec_ids

        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Switching to smart fallback.")
            return self._fallback_sales_engine(user_message, products, user_lang)

    async def process_voice_message(
        self,
        session: AsyncSession,
        voice_bytes: bytes,
        mime_type: str = "audio/ogg",
        user_lang: str = "uz"
    ) -> Tuple[str, str, List[int]]:
        """
        Process incoming voice note: transcribe and generate consultative response.
        Returns (transcription, response_text, recommended_product_ids).
        """
        if not self._configured or not self.api_key:
            return (
                "Ovozli xabar qabul qilindi",
                (
                    "Ovozli xabaringiz qabul qilindi! AI ovozli tahlil tizimi to'liq ishlashi uchun "
                    "Gemini API kaliti faollashtirilishi kerak. Ungacha menyudagi tugmalar orqali qulay xarid qilishingiz mumkin."
                ),
                []
            )

        try:
            products = await CatalogService.get_all_active_products_summary(session)
            catalog_lines = [
                f"- ID: {p['id']} | Nomi: {p['name']} | Narxi: {format_currency(p['price'])} so'm | Tavsif: {p['description']}"
                for p in products
            ]
            catalog_str = "\n".join(catalog_lines)

            system_instruction = (
                f"Siz '{settings.STORE_NAME}' do'koni uchun ovozli xabarlarni qabul qiluvchi aqlli AI Sotuvchisiz.\n"
                f"Do'konda mavjud tovarlar:\n{catalog_str}\n\n"
                f"Vazifangiz:\n"
                f"1. Ovozli xabarni matnga o'giring (transcribe qiling).\n"
                f"2. Mijoz savoliga do'kondagi mahsulotlar asosida samimiy, professional sotuvchi sifatida javob bering.\n"
                f"3. Natijani quyidagi JSON formatida qaytaring:\n"
                f'{{"transcription": "Mijoz aytgan matn", "response": "Sotuvchining javobi", "recommended_ids": [1, 2]}}\n'
                f"Faqat JSON qaytaring!"
            )

            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )

            audio_part = {
                "mime_type": mime_type,
                "data": voice_bytes
            }

            resp = await model.generate_content_async([
                audio_part,
                "Ushbu audio xabarni tahlil qiling va sotuvchi sifatida javob bering."
            ])
            text = resp.text.strip()
            # Clean markdown code blocks if any
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\n?", "", text)
                text = re.sub(r"\n?```$", "", text)

            data = json.loads(text)
            return (
                data.get("transcription", ""),
                data.get("response", ""),
                data.get("recommended_ids", [])
            )
        except Exception as e:
            logger.error(f"Error processing voice message with Gemini: {e}")
            return (
                "Ovozli xabar",
                "Ovozli xabaringiz qabul qilindi. Sizga qanday mahsulot kerakligini quyidagi katalog orqali ham tanlashingiz mumkin!",
                []
            )

    def _fallback_sales_engine(
        self,
        message: str,
        products: List[dict],
        lang: str = "uz"
    ) -> Tuple[str, List[int]]:
        """
        Intelligent offline heuristic matcher for sales inquiries.
        """
        msg_lower = message.lower()
        matched_ids = []

        # Cross-lingual synonym groups
        synonym_groups = [
            {"iphone", "айфон"},
            {"samsung", "самсунг"},
            {"airpods", "аирподс", "quloqchin", "наушник", "наушники"},
            {"macbook", "макбук"},
            {"asus", "асус"},
            {"noutbuk", "ноутбук", "laptop"},
            {"telefon", "телефон", "смартфон", "smartfon"},
            {"anker", "анкер", "powerbank", "пауэрбанк", "zaryad", "заряд"},
            {"nike", "найк", "krossovka", "кроссовки", "обувь", "poyabzal", "xudi", "худи", "kiyim", "одежда"}
        ]

        for p in products:
            target_str = f"{p['name']} {p['description']} {p['category']}".lower()

            for group in synonym_groups:
                # If user message mentions any word in this group
                if any(word in msg_lower for word in group):
                    # And this product matches any word in this group
                    if any(word in target_str for word in group):
                        if p["id"] not in matched_ids:
                            matched_ids.append(p["id"])

        if matched_ids:
            # Build consultative recommendation
            matched_prods = [p for p in products if p["id"] in matched_ids][:3]
            rec_texts = []
            for p in matched_prods:
                rec_texts.append(f"✨ **{p['name']}** — {format_currency(p['price'])} so'm\n   {p['description'][:100]}...")

            if lang == "ru":
                resp = (
                    "Отличный выбор! По вашему запросу я рекомендую следующие проверенные товары:\n\n"
                    + "\n\n".join(rec_texts) +
                    "\n\nВсе товары оригинальные и в наличии. Желаете добавить в корзину или узнать подробнее?"
                )
            else:
                resp = (
                    "Ajoyib tanlov! Sizning so'rovingiz bo'yicha quyidagi sifatli mahsulotlarni tavsiya qilaman:\n\n"
                    + "\n\n".join(rec_texts) +
                    "\n\nBarcha tovarlar original va kafolatga ega. Savatga qo'shishni xohlaysizmi?"
                )
            return resp, matched_ids[:3]

        # General questions (delivery, payment, greeting)
        if any(w in msg_lower for w in ["salom", "assalom", "privet", "hello"]):
            if lang == "ru":
                resp = (
                    f"Здравствуйте! Я AI продавец-консультант магазина '{settings.STORE_NAME}'. "
                    f"Готов помочь вам выбрать технику, аксессуары или одежду. Какой товар вас интересует?"
                )
            else:
                resp = (
                    f"Assalomu alaykum! Men '{settings.STORE_NAME}' do'konining AI sotuvchisiman. "
                    f"Sizga eng yaxshi mahsulotlarimizni tavsiya qilishga tayyorman. Qanday tovar qidiryapsiz?"
                )
            return resp, [p["id"] for p in products[:2]]

        if any(w in msg_lower for w in ["yetkaz", "dostavka", "yetkazib"]):
            if lang == "ru":
                resp = (
                    f"Доставка осуществляется по всей республике в течение 1-2 дней. "
                    f"Стоимость доставки составляет {format_currency(settings.DELIVERY_PRICE)} сум. "
                    f"При оформлении заказа просто укажите ваш адрес или отправьте геолокацию!"
                )
            else:
                resp = (
                    f"Yetkazib berish xizmati butun respublika bo'ylab 1-2 kunda amalga oshiriladi. "
                    f"Yetkazib berish narxi: {format_currency(settings.DELIVERY_PRICE)} so'm. "
                    f"Buyurtma berish paytida manzilingizni yuborishingiz kifoya!"
                )
            return resp, []

        if any(w in msg_lower for w in ["to'lov", "oplata", "click", "payme", "naqd"]):
            if lang == "ru":
                resp = "Мы принимаем оплату наличными при получении, а также через платежные системы Click и Payme."
            else:
                resp = "To'lovni mahsulotni qabul qilib olganingizda naqd pulda yoki Click va Payme orqali amalga oshirishingiz mumkin."
            return resp, []

        # Default helpful guide
        sample_ids = [p["id"] for p in products[:2]]
        if lang == "ru":
            resp = (
                f"Спасибо за ваше обращение! В нашем магазине '{settings.STORE_NAME}' представлен широкий ассортимент "
                f"электроники, гаджетов и стильных аксессуаров. Нажмите '🛍 Каталог товаров', чтобы ознакомиться с полным списком, "
                f"или напишите интересующий вас товар, например 'iPhone' или 'ноутбук'!"
            )
        else:
            resp = (
                f"Murojaatingiz uchun rahmat! '{settings.STORE_NAME}' do'konimizda zamonaviy smartfonlar, "
                f"noutbuklar va sifatli aksessuarlar mavjud. To'liq ro'yxatni ko'rish uchun quyidagi "
                f"'🛍 Mahsulotlar katalogi' tugmasini bosing yoki qiziqtirgan tovaringiz nomini yozing!"
            )
        return resp, sample_ids


gemini_sales_service = GeminiSalesService()
