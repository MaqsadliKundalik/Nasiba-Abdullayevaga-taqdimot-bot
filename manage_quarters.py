"""
Chorak sozlamalarini boshqarish scripti
"""

import asyncio
from tortoise import Tortoise
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings

async def manage_quarters():
    """Choraklar bilan ishlash"""
    try:
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models.all_models']}
        )
        
        # Hozirgi holatni ko'rsatish
        quarter_settings = await QuarterSettings.first()
        current_quarter = quarter_settings.current_quarter if quarter_settings else 1
        
        print(f"⚙️ Hozirgi chorak: {current_quarter}")
        
        # Foydalanuvchilarning chorak obunalarini ko'rsatish
        users = await User.all()
        print(f"\n👥 Foydalanuvchilar va ularning obunalari:")
        
        for user in users:
            quarters = await UserQuarterSubscription.filter(user=user, is_active=True).all()
            quarters_list = [q.quarter_number for q in quarters]
            print(f"   {user.name}: {quarters_list}")
        
        print(f"\n📝 Amallar:")
        print(f"1. Hozirgi chorakni o'zgartirish")
        print(f"2. Foydalanuvchiga hozirgi chorak obunasini berish")
        print(f"3. Chiqish")
        
        choice = input("\n❓ Tanlovingiz (1-3): ")
        
        if choice == "1":
            new_quarter = int(input("🔄 Yangi chorak raqami (1-4): "))
            if 1 <= new_quarter <= 4:
                if quarter_settings:
                    quarter_settings.current_quarter = new_quarter
                    await quarter_settings.save()
                else:
                    await QuarterSettings.create(current_quarter=new_quarter)
                print(f"✅ Chorak {new_quarter} ga o'zgartirildi")
            else:
                print("❌ Noto'g'ri chorak raqami")
        
        elif choice == "2":
            user_name = input("👤 Foydalanuvchi nomi: ")
            user = await User.get_or_none(name=user_name)
            
            if user:
                # Hozirgi chorak obunasini berish
                existing = await UserQuarterSubscription.get_or_none(
                    user=user, quarter_number=current_quarter, is_active=True
                )
                
                if existing:
                    print(f"⚠️  {user.name} da allaqachon {current_quarter}-chorak obunasi bor")
                else:
                    await UserQuarterSubscription.create(
                        user=user,
                        quarter_number=current_quarter,
                        is_active=True
                    )
                    print(f"✅ {user.name} ga {current_quarter}-chorak obunasi berildi")
            else:
                print("❌ Foydalanuvchi topilmadi")
        
        elif choice == "3":
            print("👋 Xayr!")
        
        else:
            print("❌ Noto'g'ri tanlov")
            
    except Exception as e:
        print(f"❌ Xatolik: {e}")
    
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(manage_quarters())