"""
PREMIUM FOYDALANUVCHILARNI KO'CHIRISH SCRIPTI

Bu script quyidagi vazifalarni bajaradi:
1. Eski premium foydalanuvchilarni topadi
2. Ularga 1-chorak obunasini beradi
3. Batafsil hisobot beradi

ISHLATISH:
python migrate_premium_users.py

EHTIYOT CHORALARI:
- Script ishlatishdan oldin ma'lumotlar bazasini backup qiling
- Test muhitida avval sinab ko'ring
- Script bir marta ishlatilishi kerak
"""

import asyncio
from datetime import datetime
from tortoise import Tortoise
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings

class PremiumMigrationScript:
    def __init__(self):
        self.total_premium_users = 0
        self.migrated_count = 0
        self.already_migrated_count = 0
        self.errors = []

    async def init_database(self):
        """Ma'lumotlar bazasini ishga tushirish"""
        try:
            await Tortoise.init(
                db_url='sqlite://db.sqlite3',
                modules={'models': ['database.models.all_models']}
            )
            print("✅ Ma'lumotlar bazasi muvaffaqiyatli ulandi")
            return True
        except Exception as e:
            print(f"❌ Ma'lumotlar bazasiga ulanishda xatolik: {e}")
            return False

    async def check_quarter_settings(self):
        """Chorak sozlamalarini tekshirish"""
        quarter_settings = await QuarterSettings.first()
        
        if not quarter_settings:
            quarter_settings = await QuarterSettings.create(current_quarter=1)
            print("✅ Default chorak sozlamalari yaratildi (1-chorak)")
        else:
            print(f"📊 Hozirgi faol chorak: {quarter_settings.current_quarter}")
        
        return quarter_settings

    async def get_premium_users_info(self):
        """Premium foydalanuvchilar haqida ma'lumot olish"""
        premium_users = await User.filter(is_premium=True).all()
        self.total_premium_users = len(premium_users)
        
        print(f"📊 Jami premium foydalanuvchilar: {self.total_premium_users}")
        
        if premium_users:
            print("👥 Premium foydalanuvchilar ro'yxati:")
            for i, user in enumerate(premium_users[:10], 1):  # Faqat birinchi 10 tani ko'rsatish
                print(f"   {i}. {user.name} (ID: {user.tg_id}) - Ro'yxatdan o'tgan: {user.created_at.date()}")
            
            if len(premium_users) > 10:
                print(f"   ... va yana {len(premium_users) - 10} ta foydalanuvchi")
        
        return premium_users

    async def migrate_single_user(self, user):
        """Bitta foydalanuvchini ko'chirish"""
        try:
            # 1-chorak obunasi bor yoki yo'qligini tekshir
            existing_subscription = await UserQuarterSubscription.get_or_none(
                user=user,
                quarter_number=1,
                is_active=True
            )
            
            if existing_subscription:
                print(f"⚠️  {user.name} - allaqachon 1-chorak obunasi mavjud")
                self.already_migrated_count += 1
                return "already_exists"
            else:
                # 1-chorak obunasini yarat
                await UserQuarterSubscription.create(
                    user=user,
                    quarter_number=1,
                    is_active=True
                )
                print(f"✅ {user.name} - 1-chorak obunasi muvaffaqiyatli berildi")
                self.migrated_count += 1
                return "migrated"
                
        except Exception as e:
            error_msg = f"❌ {user.name} (ID: {user.tg_id}) - Xatolik: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
            return "error"

    async def migrate_all_premium_users(self):
        """Barcha premium foydalanuvchilarni ko'chirish"""
        print("\n🔄 Ko'chirish jarayoni boshlandi...\n")
        
        premium_users = await User.filter(is_premium=True).all()
        
        for user in premium_users:
            await self.migrate_single_user(user)
        
        print(f"\n🔄 Ko'chirish jarayoni yakunlandi!")

    async def show_final_report(self):
        """Yakuniy hisobot"""
        print("\n" + "="*50)
        print("📊 YAKUNIY HISOBOT")
        print("="*50)
        print(f"📈 Jami premium foydalanuvchilar: {self.total_premium_users}")
        print(f"✅ Ko'chirilgan foydalanuvchilar: {self.migrated_count}")
        print(f"⚠️  Allaqachon mavjud: {self.already_migrated_count}")
        print(f"❌ Xatoliklar: {len(self.errors)}")
        print(f"📊 Foiz: {(self.migrated_count / self.total_premium_users * 100) if self.total_premium_users > 0 else 0:.1f}%")
        
        if self.errors:
            print(f"\n❌ Xatoliklar ro'yxati:")
            for error in self.errors:
                print(f"   {error}")
        
        print(f"\n⏰ Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)

    async def run(self):
        """Scriptni ishga tushirish"""
        print("🚀 PREMIUM FOYDALANUVCHILARNI KO'CHIRISH SCRIPTI")
        print("="*50)
        print(f"⏰ Boshlangan vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Ma'lumotlar bazasini ishga tushirish
        if not await self.init_database():
            return
        
        try:
            # Chorak sozlamalarini tekshirish
            await self.check_quarter_settings()
            print()
            
            # Premium foydalanuvchilar ma'lumotini olish
            premium_users = await self.get_premium_users_info()
            
            if not premium_users:
                print("❌ Premium foydalanuvchilar topilmadi!")
                return
            
            # Tasdiqlash
            confirm = input(f"\n❓ {self.total_premium_users} ta premium foydalanuvchini ko'chirishni istaysizmi? (y/N): ")
            if confirm.lower() not in ['y', 'yes', 'ha']:
                print("🚫 Script bekor qilindi")
                return
            
            # Ko'chirish jarayoni
            await self.migrate_all_premium_users()
            
            # Yakuniy hisobot
            await self.show_final_report()
            
        except Exception as e:
            print(f"❌ Umumiy xatolik: {e}")
        
        finally:
            await Tortoise.close_connections()
            print("\n🔐 Ma'lumotlar bazasi ulanishi yopildi")

async def main():
    script = PremiumMigrationScript()
    await script.run()

if __name__ == "__main__":
    asyncio.run(main())