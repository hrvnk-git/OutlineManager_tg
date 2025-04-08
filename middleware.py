import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from dotenv import load_dotenv

load_dotenv()
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))


class AuthorizedUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            if event.from_user.id == AUTHORIZED_USER_ID:
                return await handler(event, data)
            else:
                await event.answer(
                    "```Ошибка! У вас нет доступа к этому боту.```",
                    parse_mode="Markdown",
                )
                return
