from aiogram import Bot
from aiogram.types import FSInputFile
from asyncio import run
import os

async def send_database():
    bot = Bot(token="8089197582:AAHIX6oYt_WT97p1Q0laQbFL5vKd7tCqZfk")
    
    try:
        # Fayl yo'lini aniqlash
        db_path = os.path.join(os.getcwd(), "db.sqlite3")
        
        # Fayl mavjudligini tekshirish
        if os.path.exists(db_path):
            print(f"📁 Fayl topildi: {db_path}")
            
            # Fayl hajmini ko'rsatish
            file_size = os.path.getsize(db_path)
            print(f"📊 Fayl hajmi: {file_size} bayt")
            
            # FSInputFile orqali fayl yuborish
            document = FSInputFile(db_path, filename="database.sqlite3")
            
            await bot.send_document(
                chat_id=5165396993,
                document=document,
                caption=f"📄 Ma'lumotlar bazasi fayli\n📊 Hajm: {file_size} bayt"
            )
            print("✅ Ma'lumotlar bazasi muvaffaqiyatli yuborildi!")
            
        else:
            print(f"❌ Fayl topilmadi: {db_path}")
            print("💡 Iltimos, fayl yo'lini tekshiring")
    
    except Exception as e:
        print(f"❌ Xatolik: {e}")
    
    finally:
        # Session ni yopish
        await bot.session.close()
        print("🔐 Bot session yopildi")

if __name__ == "__main__":
    run(send_database())