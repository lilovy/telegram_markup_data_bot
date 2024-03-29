from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from config import TOKEN, WEBAPP_HOST
from src.server.bot import dp, bot


app = FastAPI()
WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = WEBAPP_HOST + WEBHOOK_PATH


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.feed_update(Bot, telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()