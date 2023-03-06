from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncScalarResult,
    )

from config import ACCESS_ID, ADMIN_ID
from ...db.models.async_models import User
from ..handlers.handler_config import (
    # GuestAccess,
    UserAccess,
    AdminAccess,
    AccessLevel,
)



class Permission:
    
    user = 'user'
    guest = 'guest'
    admin = 'admin'


class Access(BaseMiddleware):
    def __init__(
        self,
        admin_id: int = ADMIN_ID,
        access_id: list = ACCESS_ID,
        ):
        self.admin_id = admin_id
        self.access_id = access_id
        super().__init__()

    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
        ) -> Any:
        
        user = await GetUser(
            user_id=event.from_user.id,
            username=event.from_user.username,
            session=data['session_maker']).return_user()

        # sessinon_maker: async_sessionmaker = data['session_maker']
        
        # async with sessinon_maker() as session:
        #     async with session.begin():

        #         session: AsyncSession
        #         stmt = select(User).where(User.id == event.from_user.id)
        #         result = await session.scalars(stmt)

        #         result: AsyncScalarResult
        #         user: User = result.one_or_none()

        #         if not user:

        #             permission = Permission().user
                    
        #             if event.from_user.id == self.admin_id:
        #                 permission = Permission().admin
        #             if event.from_user.id in self.access_id:
        #                 permission = Permission().user

        #             user = User(
        #                 id=event.from_user.id,
        #                 username=event.from_user.username,
        #                 permission=permission,
        #                 )

        #             await session.merge(user)

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
        session: async_sessionmaker,
        ):
        self.user_id = user_id
        self.username = username
        self.session = session
    
    async def _create_user(self):
        
        async with self.session() as session:
            async with session.begin():
                session: AsyncSession

                permission = Permission().guest

                if self.user_id == self.admin_id:
                    permission = Permission().admin
                elif self.user_id in self.access_id:
                    permission = Permission().user

                user = User(
                    id=self.user_id,
                    username=self.username,
                    permission=permission,
                    )

                await session.merge(user)
        return user        

    async def _return_user(self):
        async with self.session() as session:
            async with session.begin():
                session: AsyncSession
                stmt = select(User).where(User.id == self.user_id)
                result = await session.scalars(stmt)

                result: AsyncScalarResult
                user: User = result.one_or_none()
                
        return user
        
    async def return_user(
        self,
        ) -> User:
        user = await self._return_user()

        if not user:
            user = await self._create_user()
        
        return user

        ...

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
        
        if user.permission == Permission().admin:
            return await handler(event, data) 

        elif user.permission == Permission().user:

            if event.text not in AccessLevel().user:
                return await handler(event, data)
            else:
                await denied

        elif user.permission == Permission().guest:

            if event.text not in AccessLevel().guest:
                return await handler(event, data)
            else:
                await denied
        else:
            await denied