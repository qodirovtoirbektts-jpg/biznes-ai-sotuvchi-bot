from bot.services.gemini_sales import GeminiSalesService


def test_sales_service_fallback_matching():
    service = GeminiSalesService()
    sample_products = [
        {
            "id": 1,
            "name": "iPhone 15 Pro Max",
            "category": "Smartfonlar",
            "price": 15000000,
            "stock": 5,
            "description": "Eng zo'r kamera va titan korpus"
        },
        {
            "id": 2,
            "name": "MacBook Air M3",
            "category": "Noutbuklar",
            "price": 18000000,
            "stock": 3,
            "description": "Kuchli va yupqa noutbuk"
        }
    ]

    # Test Uzbek query
    resp_uz, ids_uz = service._fallback_sales_engine(
        "Menga yaxshi telefon kerak, iPhone bormi?",
        sample_products,
        lang="uz"
    )
    assert 1 in ids_uz
    assert "iPhone 15 Pro Max" in resp_uz

    # Test Russian query with keyword 'ноутбук'
    resp_ru, ids_ru = service._fallback_sales_engine(
        "Подскажите, есть ли в наличии ноутбук для учебы?",
        sample_products,
        lang="ru"
    )
    assert 2 in ids_ru
    assert "MacBook Air" in resp_ru

    # Test Delivery query
    resp_deliv, _ = service._fallback_sales_engine(
        "Yetkazib berish xizmati qanday ishlaydi?",
        sample_products,
        lang="uz"
    )
    assert "Yetkazib berish xizmati" in resp_deliv
