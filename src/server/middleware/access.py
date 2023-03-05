from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncScalarResult,
    )

from config import ACCESS_ID
from ...db.models.async_models import User


class Permission:
    
    user = 'user'
    guest = 'guest'
    admin = 'admin'


class Access(BaseMiddleware):
    def __init__(
        self,
        handlers: list,
        access_id: list = ACCESS_ID,
        ):
        self.access_id = access_id
        self.handlers = handlers
        super().__init__()

    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
        ) -> Any:
        

        sessinon_maker: async_sessionmaker = data['session_maker']
        
        async with sessinon_maker() as session:
            async with session.begin():

                session: AsyncSession
                stmt = select(User).where(User.id == event.from_user.id)
                result = await session.scalars(stmt)

                result: AsyncScalarResult
                user: User = result.one_or_none()

                if not user:

                    permission = Permission.user
                    
                    if event.from_user.id in self.access_id:
                        permission = Permission.admin

                    # session.add(
                    #     User(
                    #         id=event.from_user.id,
                    #         username=event.from_user.username,
                    #         permission=permission,
                    #         )
                    #     )

                    user = User(
                        id=event.from_user.id,
                        username=event.from_user.username,
                        permission=permission,
                        )

                    await session.merge(user)

        if event.text in self.handlers:
            if user.permission == Permission.admin:
                return await handler(event, data)
            else:
                await event.answer(
                    'Access denied.\n' \
                    'contact @obama for access',
                    show_alert=True
                )
                return

        if user.permission in (Permission.user, Permission.admin):
            return await handler(event, data)

        await event.answer(
            'Access denied.\n' \
            'contact @obama for access',
            show_alert=True
        )
        return