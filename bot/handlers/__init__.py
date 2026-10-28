from aiogram import Router
from bot.handlers.common import router as common_router
from bot.handlers.admin import router as admin_router
from bot.handlers.catalog import router as catalog_router
from bot.handlers.cart import router as cart_router
from bot.handlers.checkout import router as checkout_router
from bot.handlers.orders import router as orders_router
from bot.handlers.voice import router as voice_router
from bot.handlers.ai_chat import router as ai_chat_router


def setup_routers() -> Router:
    main_router = Router()
    # Order matters: specific commands and buttons first, catch-all AI chat last
    main_router.include_router(common_router)
    main_router.include_router(admin_router)
    main_router.include_router(catalog_router)
    main_router.include_router(cart_router)
    main_router.include_router(checkout_router)
    main_router.include_router(orders_router)
    main_router.include_router(voice_router)
    main_router.include_router(ai_chat_router)
    return main_router
