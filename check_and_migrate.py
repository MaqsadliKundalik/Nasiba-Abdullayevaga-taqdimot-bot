"""
Ma'lumotlar bazasini tekshirish va premium foydalanuvchilarni ko'rish scripti
"""

import asyncio
import sqlite3
from tortoise import Tortoise
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings, PresentationFiles

async def check_database():
    """Ma'lumotlar bazasini tekshirish"""
    print("🔍 Ma'lumotlar bazasini tekshirish...\n")
    
    try:
        # Tortoise ORM bilan ulanish
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models.all_models']}
        )
        print("✅ Ma'lumotlar bazasiga ulanish muvaffaqiyatli")
        
        # Jadvallari yaratish (agar mavjud bo'lmasa)
        await Tortoise.generate_schemas()
        print("✅ Jadval strukturalari tekshirildi")
        
        # Statistikalarni olish
        total_users = await User.all().count()
        premium_users = await User.filter(is_premium=True).count()
        quarter_subscriptions = await UserQuarterSubscription.all().count()
        presentations = await PresentationFiles.all().count()
        
        print(f"\n📊 MA'LUMOTLAR BAZASI STATISTIKASI:")
        print(f"👥 Jami foydalanuvchilar: {total_users}")
        print(f"💎 Premium foydalanuvchilar: {premium_users}")
        print(f"📚 Chorak obunalari: {quarter_subscriptions}")
        print(f"📂 Taqdimotlar: {presentations}")
        
        # Premium foydalanuvchilar ro'yxati
        if premium_users > 0:
            print(f"\n👑 PREMIUM FOYDALANUVCHILAR:")
            premium_list = await User.filter(is_premium=True).all()
            
            for i, user in enumerate(premium_list, 1):
                # Bu foydalanuvchining chorak obunalarini tekshir
                user_quarters = await UserQuarterSubscription.filter(user=user, is_active=True).all()
                quarters_text = ", ".join([f"{q.quarter_number}-chorak" for q in user_quarters]) if user_quarters else "Yo'q"
                
                print(f"   {i}. {user.name} (ID: {user.tg_id})")
                print(f"      📱 Telefon: {user.phone_number}")
                print(f"      📚 Chorak obunalari: {quarters_text}")
                print(f"      📅 Ro'yxatdan o'tgan: {user.created_at.date()}")
                print()
        
        # Chorak sozlamalarini tekshir
        quarter_settings = await QuarterSettings.first()
        if quarter_settings:
            print(f"⚙️ Hozirgi chorak: {quarter_settings.current_quarter}")
        else:
            print("⚠️ Chorak sozlamalari mavjud emas")
        
        return total_users, premium_users, quarter_subscriptions
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return 0, 0, 0
    
    finally:
        await Tortoise.close_connections()

async def migrate_premium_to_quarter():
    """Premium foydalanuvchilarni 1-chorakga ko'chirish"""
    print("\n🔄 Premium foydalanuvchilarni 1-chorakga ko'chirish...\n")
    
    try:
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models.all_models']}
        )
        
        # Chorak sozlamalarini yaratish (agar mavjud bo'lmasa)
        quarter_settings = await QuarterSettings.first()
        if not quarter_settings:
            await QuarterSettings.create(current_quarter=1)
            print("✅ Chorak sozlamalari yaratildi (1-chorak)")
        
        # Premium foydalanuvchilarni olish
        premium_users = await User.filter(is_premium=True).all()
        
        if not premium_users:
            print("❌ Premium foydalanuvchilar topilmadi")
            return
        
        migrated_count = 0
        already_exists_count = 0
        
        for user in premium_users:
            # 1-chorak obunasi bor yoki yo'qligini tekshir
            existing_subscription = await UserQuarterSubscription.get_or_none(
                user=user,
                quarter_number=1,
                is_active=True
            )
            
            if existing_subscription:
                print(f"⚠️  {user.name} - allaqachon 1-chorak obunasi mavjud")
                already_exists_count += 1
            else:
                # 1-chorak obunasini yaratish
                await UserQuarterSubscription.create(
                    user=user,
                    quarter_number=1,
                    is_active=True
                )
                print(f"✅ {user.name} - 1-chorak obunasi berildi")
                migrated_count += 1
        
        print(f"\n📈 NATIJALAR:")
        print(f"✅ Ko'chirilgan: {migrated_count}")
        print(f"⚠️  Allaqachon mavjud: {already_exists_count}")
        print(f"📊 Jami: {len(premium_users)}")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
    
    finally:
        await Tortoise.close_connections()

async def main():
    print("🚀 MA'LUMOTLAR BAZASINI TEKSHIRISH VA MIGRATION SCRIPTI")
    print("=" * 60)
    
    # Ma'lumotlar bazasini tekshirish
    total, premium, quarters = await check_database()
    
    if premium > 0:
        print("\n" + "=" * 60)
        confirm = input("❓ Premium foydalanuvchilarni 1-chorakga ko'chirishni istaysizmi? (y/N): ")
        
        if confirm.lower() in ['y', 'yes', 'ha']:
            await migrate_premium_to_quarter()
        else:
            print("🚫 Ko'chirish bekor qilindi")
    
    print("\n🎉 Script yakunlandi!")

if __name__ == "__main__":
    asyncio.run(main())