"""
Ma'lumotlar bazasidagi barcha foydalanuvchilarni ko'rish
"""

import asyncio
from tortoise import Tortoise
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings

async def show_all_users():
    """Barcha foydalanuvchilarni ko'rsatish"""
    try:
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models.all_models']}
        )
        
        print("👥 BARCHA FOYDALANUVCHILAR:\n")
        
        users = await User.all()
        
        if not users:
            print("❌ Foydalanuvchilar topilmadi")
            return
        
        for i, user in enumerate(users, 1):
            # Chorak obunalarini olish
            quarters = await UserQuarterSubscription.filter(user=user, is_active=True).all()
            quarters_text = ", ".join([f"{q.quarter_number}-chorak" for q in quarters]) if quarters else "Yo'q"
            
            print(f"{i}. 👤 {user.name}")
            print(f"   📱 Telefon: {user.phone_number}")
            print(f"   🆔 Telegram ID: {user.tg_id}")
            print(f"   💎 Premium: {'✅ Ha' if user.is_premium else '❌ Yo''q'}")
            print(f"   📚 Chorak obunalari: {quarters_text}")
            print(f"   📅 Ro'yxatdan o'tgan: {user.created_at}")
            print("-" * 50)
        
        # Agar premium bo'lmagan foydalanuvchilar bo'lsa, ularni premium qilish taklifi
        non_premium_users = await User.filter(is_premium=False).all()
        
        if non_premium_users:
            print(f"\n📊 {len(non_premium_users)} ta oddiy foydalanuvchi topildi")
            confirm = input("❓ Ularni premium qilishni istaysizmi? (y/N): ")
            
            if confirm.lower() in ['y', 'yes', 'ha']:
                for user in non_premium_users:
                    user.is_premium = True
                    await user.save()
                    
                    # 1-chorak obunasini berish
                    existing_quarter = await UserQuarterSubscription.get_or_none(
                        user=user, quarter_number=1, is_active=True
                    )
                    
                    if not existing_quarter:
                        await UserQuarterSubscription.create(
                            user=user,
                            quarter_number=1,
                            is_active=True
                        )
                    
                    print(f"✅ {user.name} - premium va 1-chorak obunasi berildi")
                
                print(f"\n🎉 {len(non_premium_users)} ta foydalanuvchi premium qilindi!")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
    
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(show_all_users())