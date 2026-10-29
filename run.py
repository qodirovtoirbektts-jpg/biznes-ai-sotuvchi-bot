import asyncio
import logging
import os
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import settings
from bot.database.session import init_db
from bot.middlewares.user_middleware import UserAndDbMiddleware
from bot.handlers import setup_routers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("sotuvchi_bot")


async def health_handler(request: web.Request) -> web.Response:
    """Render health check endpoint."""
    return web.json_response({
        "status": "ok",
        "service": "Biznes AI Sotuvchi Bot",
        "bot": "@Ai_sotuvchii_bot"
    })


async def start_render_health_server(port: int) -> web.AppRunner:
    """Start lightweight HTTP server for Render free web service health checks."""
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Render health check server successfully started on port {port}")
    return runner


async def keep_alive_pinger():
    """Periodically ping external URL to keep service active on free tiers."""
    ping_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("KEEP_ALIVE_URL")
    if not ping_url:
        return
    if not ping_url.endswith("/health"):
        ping_url = f"{ping_url.rstrip('/')}/health"

    logger.info(f"Keep-alive pinger faollashtirildi: {ping_url}")
    await asyncio.sleep(60)
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ping_url, timeout=15) as resp:
                    logger.info(f"Keep-alive pinger javobi: HTTP {resp.status}")
        except Exception as exc:
            logger.debug(f"Keep-alive pinger bildirishnomasi: {exc}")
        await asyncio.sleep(600)  # Ping every 10 minutes


async def main():
    bot_token = settings.BOT_TOKEN or os.getenv("BOT_TOKEN") or "9277921986:AAFriz9__oOJgaqrhNdW3NeIfjdg1jZcBM8"
    if not bot_token:
        logger.error("BOT_TOKEN is not provided!")
        return

    logger.info("Initializing database...")
    await init_db()
    logger.info("Database successfully initialized.")

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    dp = Dispatcher(storage=MemoryStorage())

    # Global error handler so no uncaught handler exception crashes the bot
    @dp.error()
    async def global_error_handler(event):
        logger.error(f"Ushlangan ichki xatolik: {event.exception}", exc_info=True)
        return True

    # Register Middlewares
    user_middleware = UserAndDbMiddleware()
    dp.message.middleware(user_middleware)
    dp.callback_query.middleware(user_middleware)

    # Register Handlers
    dp.include_router(setup_routers())

    # Start optional Render port listener if $PORT is defined
    web_runner = None
    port_env = os.getenv("PORT")
    if port_env and port_env.isdigit():
        web_runner = await start_render_health_server(int(port_env))

    # Start background keep-alive pinger
    pinger_task = asyncio.create_task(keep_alive_pinger())

    # Delete webhook and drop pending updates before starting polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        logger.warning(f"Webhook tozalashda ogohlantirish: {e}")

    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot muvaffaqiyatli ishga tushdi: @{bot_info.username} ({bot_info.first_name})")
    except Exception as e:
        logger.warning(f"Bot ma'lumotlarini olishda ogohlantirish: {e}")

    # Resilient polling loop with auto-reconnection
    try:
        while True:
            try:
                logger.info("Bot xabarlarni qabul qilishga tayyor (polling faol)...")
                await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
                break
            except (KeyboardInterrupt, SystemExit):
                logger.info("Bot to'xtatildi.")
                break
            except Exception as exc:
                logger.error(f"Aloqa uzildi yoki xatolik: {exc}. 5 soniyadan so'ng qayta ulanadi...")
                await asyncio.sleep(5)
    finally:
        pinger_task.cancel()
        if web_runner:
            await web_runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'liq to'xtatildi.")
