from aiogram import Bot, Dispatcher
from asyncio import run, create_task
from config import TOKEN
from logging import basicConfig, INFO
from database.database_init import init_db
import handlers

dp = Dispatcher()
dp.include_router(handlers.router)

async def main():
    bot = Bot(token=TOKEN)
    await init_db()
    await dp.start_polling(bot)

basicConfig(level=INFO)
run(main())