from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from asyncio import run
import os

async def startup(bot: Bot):
    # Fayl yo'lini to'g'ri aniqlash
    db_path = os.path.join(os.getcwd(), "db.sqlite3")
    
    # Fayl mavjudligini tekshirish
    if os.path.exists(db_path):
        # FSInputFile dan foydalanish
        document = FSInputFile(db_path)
        await bot.send_document(
            chat_id=5165396993,
            document=document,
            caption="Ma'lumotlar bazasi fayli"
        )
        print("✅ Fayl yuborildi")
    else:
        print(f"❌ Fayl topilmadi: {db_path}")

dp = Dispatcher()

async def main():
    bot = Bot(token="8089197582:AAHIX6oYt_WT97p1Q0laQbFL5vKd7tCqZfk")
    
    try:
        dp.startup.register(startup)
        await dp.start_polling(bot)
    finally:
        # Session ni to'g'ri yopish
        await bot.session.close()

if __name__ == "__main__":
    run(main())