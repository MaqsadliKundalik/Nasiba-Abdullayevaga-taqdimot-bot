"""
Premium foydalanuvchilarni ko'rish scripti
"""

import asyncio
from tortoise import Tortoise
from database.models.all_models import User, UserQuarterSubscription

async def show_premium_users():
    """Premium foydalanuvchilarni ko'rsatish"""
    try:
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models.all_models']}
        )
        
        premium_users = await User.filter(is_premium=True).all()
        
        print(f"👑 PREMIUM FOYDALANUVCHILAR ({len(premium_users)} ta):")
        print("Bu foydalanuvchilarda 'Sizda to'liq obuna mavjud' xabari chiqadi\n")
        
        for i, user in enumerate(premium_users, 1):
            quarters = await UserQuarterSubscription.filter(user=user, is_active=True).all()
            quarters_text = ", ".join([f"{q.quarter_number}-chorak" for q in quarters]) if quarters else "Yo'q"
            
            print(f"{i:2}. {user.name}")
            print(f"    📱 Telefon: {user.phone_number}")
            print(f"    🆔 ID: {user.tg_id}")
            print(f"    📚 Chorak obunalari: {quarters_text}")
            print(f"    📅 Sana: {user.created_at.date()}")
            print()
        
        # Agar biron kimni premium dan chiqarmoqchi bo'lsak
        print("=" * 50)
        choice = input("❓ Biron kimni premium holatdan chiqarmoqchimisiz? (y/N): ")
        
        if choice.lower() in ['y', 'yes', 'ha']:
            user_name = input("👤 Foydalanuvchi nomi: ")
            user = await User.get_or_none(name=user_name)
            
            if user and user.is_premium:
                user.is_premium = False
                await user.save()
                print(f"✅ {user.name} premium holatdan chiqarildi")
            else:
                print("❌ Foydalanuvchi topilmadi yoki premium emas")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
    
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(show_premium_users())