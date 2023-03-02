import logging
from config import TOKEN, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, LOCALHOST

from aiohttp.web import run_app
from aiohttp.web_app import Application

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram import Dispatcher, Router, Bot, types, F
from aiogram.methods import SendMessage
from src.server import handlers

WEBAPP_HOST = LOCALHOST  # or ip

logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(F.text)
async def echo(message: types.Message):
    # Regular request, add bot: Bot to handler kwargs
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(chat_id=message.chat.id, text=message.text)


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
    bot = Bot(token=TOKEN, parse_mode="HTML")

    dispatcher = Dispatcher()
    dispatcher["webhook_url"] = WEBHOOK_URL
    dispatcher.include_routers(router, handlers.r)(router)

    app = Application()
    app["bot"] = bot

    # Skip updates
    # bot.delete_webhook()

    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path=WEBHOOK_PATH)
    setup_application(app, dispatcher, bot=bot)

    run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()