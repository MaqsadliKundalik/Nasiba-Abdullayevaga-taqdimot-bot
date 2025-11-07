from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.models.all_models import PresentationFiles, User, UserQuarterSubscription
from filters.users import HasQuarterAccess

router = Router()

@router.message(F.text == "Taqdimot qidirish")
async def search_presentation_info(message: Message):
    await message.answer("📂 Taqdimot qidirish uchun uning kodini yuborasiz:\n\nNa'muna: 5-1-1\nBuni men 5-sinf 1-chorak 1-dars deb tushunaman. ✅")

@router.message(F.text.regexp(r"^\d{1,2}-\d{1,2}-\d{1,2}$"))
async def search_presentation(message: Message):
    code = message.text
    parts = code.split("-")
    class_number = parts[0]
    part_number = int(parts[1])  # Chorak raqami
    lesson_number = parts[2]
    
    user = await User.get_or_none(tg_id=message.from_user.id)
    if not user:
        await message.answer("❌ Avval ro'yxatdan o'ting!")
        return
    
    # Foydalanuvchining ruxsatlarini tekshir
    has_access = False
    
    # To'liq premium tekshir
    if user.is_premium:
        has_access = True
    else:
        # Chorak obunasini tekshir
        quarter_subscription = await UserQuarterSubscription.get_or_none(
            user=user, 
            quarter_number=part_number, 
            is_active=True
        )
        if quarter_subscription:
            has_access = True
    
    if not has_access:
        await message.answer(
            f"❌ {part_number}-chorak taqdimotlariga ruxsatingiz yo'q!\n\n"
            f"Bu chorak uchun obuna harid qiling: /start"
        )
        return
    
    # Taqdimotni qidir
    presentations = await PresentationFiles.filter(
        class_number=class_number,
        part_number=part_number,
        lesson_number=lesson_number
    ).all()
    
    if presentations:
        for pres in presentations:
            await message.answer_document(
                pres.file_id,
                caption=f"📚 <b>{pres.lesson_name}</b>\n"
                    f"🏫 {pres.class_number}-sinf {pres.lesson_number}-dars ({pres.part_number}-chorak)\n"
                f"🌐 <b>Taqdimot tili:</b> {pres.file_lang}\n\n"
                f"Taqdimotlarda ko'rsatilgan fayllarni INFOTAQDIMOT kanalidan yuklab olishingiz mumkin: https://t.me/INFOTAQDIMOT\n"
                f"Attestatsiyaga tayyorlov guruhimiz: t.me/informatiklarahil",
                parse_mode="HTML",
                protect_content=True
        )
    else:
        await message.answer("❌ Taqdimot topilmadi!")
