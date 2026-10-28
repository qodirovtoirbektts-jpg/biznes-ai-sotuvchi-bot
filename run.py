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


async def main():
    if not settings.BOT_TOKEN:
        logger.error("BOT_TOKEN is not provided in .env!")
        return

    logger.info("Initializing database...")
    await init_db()
    logger.info("Database successfully initialized.")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    dp = Dispatcher(storage=MemoryStorage())

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

    # Delete webhook and drop pending updates before starting polling
    await bot.delete_webhook(drop_pending_updates=True)

    bot_info = await bot.get_me()
    logger.info(f"Bot started successfully: @{bot_info.username} ({bot_info.first_name})")

    try:
        await dp.start_polling(bot)
    finally:
        if web_runner:
            await web_runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
