from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from config import ACCESS_ID, ADMIN_ID
from ...db.models.async_models import User
from ..handlers.handler_config import (
    AccessLevel,
)
from ...db.action import save_user, get_user_info

class Permission:
    user = 'user'
    guest = 'guest'
    admin = 'admin'


class Access(BaseMiddleware):
    async def __call__(
        self, 
        handler,
        event,
        data,
        ) -> Any:

        user = await GetUser(
            user_id=event.from_user.id,
            username=event.from_user.username,
            ).return_user()

        await CheckPermission().check(
            user,
            handler, 
            event, 
            data,
            )
        return


class GetUser:
    def __init__(
        self,
        user_id: int,
        username: str,
        ):
        self.user_id = user_id
        self.username = username
    
    async def _create_user(self):

        permission = Permission().guest

        if self.user_id == ADMIN_ID:
            permission = Permission().admin
        elif self.user_id in ACCESS_ID:
            permission = Permission().user

        await save_user(
            user_id=self.user_id, 
            username=self.username,
            permission=permission,
            )

    async def _return_user(self):
        
        return await get_user_info(user_id=self.user_id)

    async def return_user(
        self,
        ) -> User:
        user = await self._return_user()

        if not user:
            await self._create_user()
            user = await self._return_user()

        return user


class CheckPermission:

    async def check(
        self,
        user: User,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
        ):

        denied = event.answer(
        'Access denied.\n' \
        'contact @obama for access',
        show_alert=True,
        )
        _event = event
        if isinstance(_event, CallbackQuery):
            _event = _event.message

        if user.permission == Permission().admin:
            return await handler(event, data) 

        elif user.permission == Permission().user:

            if _event.text not in AccessLevel().user:
                return await handler(event, data)
            else:
                await denied

        elif user.permission == Permission().guest:

            if _event.text not in AccessLevel().guest:
                return await handler(event, data)
            else:
                await denied
        else:
            await denied