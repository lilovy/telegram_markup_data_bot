import logging, asyncio
from config import (
    TOKEN, 
    WEBAPP_PORT, 
    WEBHOOK_PATH, 
    WEBHOOK_URL, 
    LOCALHOST,
    ADMIN_ID,
    ACCESS_ID,
    )
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram import (
    Dispatcher, 
    Router, 
    Bot, 
    types, 
    F,
    )
from aiogram.enums import ParseMode

from ..db.db_async import async_session
from ..db.init_db import init_db
from .init import bot

from .handlers.FSM import fsm_save_data
from .middleware.access import Access

from ..server.handlers import (
    handlers, 
    tg_storage,
    last_handler,
    admin_handler,
    get_file,
    markup_handler,
    )


logging.basicConfig(level=logging.INFO)
# bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN_V2)

router = Router()
router.message.filter(F.chat.type == 'private')

@router.startup()
async def on_startup(bot: Bot, webhook_url: str):
    await bot.set_webhook(webhook_url)


@router.shutdown()
async def on_shutdown(bot: Bot, dispatcher: Dispatcher):
    logging.warning("Shutting down..")

    # Insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close bot session
    await bot.session.close()

    logging.warning("Bye!")


def main():

    init_db()

    dispatcher = Dispatcher()
    dispatcher["webhook_url"] = WEBHOOK_URL
    dispatcher['session_maker'] = async_session

    dispatcher.include_routers(
        router, 
        handlers.router, 
        fsm_save_data.router,
        admin_handler.router,
        tg_storage.router,
        get_file.router,
        markup_handler.router,
        last_handler.router,
        )

    dispatcher.message.middleware(Access())
    dispatcher.callback_query.middleware(Access())

    app = Application()
    app["bot"] = bot

    # Skip updates
    # bot.delete_webhook()

    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path=WEBHOOK_PATH)
    setup_application(app, dispatcher, bot=bot)

    run_app(app, host=LOCALHOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
