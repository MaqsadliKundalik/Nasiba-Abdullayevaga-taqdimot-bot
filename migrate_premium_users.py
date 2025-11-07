"""
Script: Eski premium foydalanuvchilarni yangi chorak tizimiga ko'chirish
Vazifasi: Barcha premium foydalanuvchilarga 1-chorak ruxsatini berish
"""

import asyncio
from tortoise import Tortoise
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings

async def init_database():
    """Ma'lumotlar bazasini ishga tushirish"""
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['database.models.all_models']}
    )
    print("✅ Ma'lumotlar bazasi ulandi")

async def migrate_premium_users():
    """Premium foydalanuvchilarni 1-chorak obunasiga ko'chirish"""
    print("🔄 Premium foydalanuvchilarni ko'chirish boshlandi...")
    
    # Barcha premium foydalanuvchilarni ol
    premium_users = await User.filter(is_premium=True).all()
    print(f"📊 Jami premium foydalanuvchilar: {len(premium_users)}")
    
    if not premium_users:
        print("❌ Premium foydalanuvchilar topilmadi!")
        return
    
    migrated_count = 0
    already_migrated_count = 0
    
    for user in premium_users:
        # 1-chorak uchun obuna bor yoki yo'qligini tekshir
        existing_subscription = await UserQuarterSubscription.get_or_none(
            user=user, 
            quarter_number=1,
            is_active=True
        )
        
        if existing_subscription:
            print(f"⚠️  {user.name} (ID: {user.tg_id}) - allaqachon 1-chorak obunasi bor")
            already_migrated_count += 1
        else:
            # 1-chorak obunasini yarat
            await UserQuarterSubscription.create(
                user=user,
                quarter_number=1,
                is_active=True
            )
            print(f"✅ {user.name} (ID: {user.tg_id}) - 1-chorak obunasi berildi")
            migrated_count += 1
    
    print(f"\n📈 Natijalar:")
    print(f"   ✅ Ko'chirilgan: {migrated_count}")
    print(f"   ⚠️  Allaqachon mavjud: {already_migrated_count}")
    print(f"   📊 Jami: {len(premium_users)}")

async def check_quarter_settings():
    """Chorak sozlamalarini tekshirish va yaratish"""
    quarter_settings = await QuarterSettings.first()
    
    if not quarter_settings:
        # Default chorak sozlamalarini yaratish
        quarter_settings = await QuarterSettings.create(current_quarter=1)
        print("✅ 1-chorak default sozlamalar yaratildi")
    else:
        print(f"📊 Hozirgi chorak: {quarter_settings.current_quarter}")

async def main():
    """Asosiy funksiya"""
    print("🚀 Premium foydalanuvchilarni ko'chirish scripti boshlandi\n")
    
    try:
        # Ma'lumotlar bazasini ishga tushirish
        await init_database()
        
        # Chorak sozlamalarini tekshirish
        await check_quarter_settings()
        
        # Premium foydalanuvchilarni ko'chirish
        await migrate_premium_users()
        
        print("\n🎉 Script muvaffaqiyatli yakunlandi!")
        
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
    finally:
        # Ma'lumotlar bazasini yopish
        await Tortoise.close_connections()
        print("🔐 Ma'lumotlar bazasi ulanishi yopildi")

if __name__ == "__main__":
    asyncio.run(main())