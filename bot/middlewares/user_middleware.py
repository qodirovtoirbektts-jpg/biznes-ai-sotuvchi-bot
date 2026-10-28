from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy import select
from bot.database.models import User
from bot.database.session import async_session_maker
from bot.config import settings


class UserAndDbMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        tg_user: TgUser = data.get("event_from_user")
        if not tg_user:
            return await handler(event, data)

        async with async_session_maker() as session:
            # Check user in DB
            stmt = select(User).where(User.id == tg_user.id)
            result = await session.execute(stmt)
            db_user = result.scalars().first()

            is_admin = tg_user.id in settings.ADMIN_IDS

            if not db_user:
                lang = tg_user.language_code or "uz"
                if lang not in ("uz", "oz", "ru"):
                    lang = "uz"

                db_user = User(
                    id=tg_user.id,
                    username=tg_user.username,
                    full_name=tg_user.full_name or "",
                    language_code=lang,
                    is_admin=is_admin
                )
                session.add(db_user)
                await session.commit()
                await session.refresh(db_user)
            else:
                # Update info if changed
                changed = False
                if db_user.username != tg_user.username:
                    db_user.username = tg_user.username
                    changed = True
                if db_user.full_name != (tg_user.full_name or ""):
                    db_user.full_name = tg_user.full_name or ""
                    changed = True
                if is_admin and not db_user.is_admin:
                    db_user.is_admin = True
                    changed = True
                if changed:
                    await session.commit()

            data["session"] = session
            data["user"] = db_user
            data["lang"] = db_user.language_code or "uz"
            data["is_admin"] = db_user.is_admin

            return await handler(event, data)
