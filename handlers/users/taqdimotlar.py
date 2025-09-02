from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.models.all_models import PresentationFiles, User
from filters.users import IsPremUser

router = Router()

@router.message(F.text == "Taqdimot qidirish")
async def f(message: Message):
    await message.answer("📂 Taqdimot qidirish uchun uning kodini yuborasiz:\n\nNa'muna: 5-1-1\nBuni men 5-sinf 1-chorak 1-dars deb tushunaman. ✅")

@router.message(IsPremUser(), F.text.regexp(r"^\d{1,2}-\d{1,2}-\d{1,2}$"))
async def f(message: Message):
    code = message.text
    lesson_number, part_number, class_number = code.split("-")
    presentation = await PresentationFiles.filter(
        lesson_number=lesson_number,
        part_number=part_number,
        class_number=class_number
    ).all()
    if presentation:
        for pres in presentation:
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

