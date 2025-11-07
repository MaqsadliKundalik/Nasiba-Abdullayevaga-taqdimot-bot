from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models.all_models import QuarterSettings
from filters.admins import IsAdmin
from keyboards.admins import quarter_settings_menu, quarter_select_menu, admin_main_menu
from states.admins import QuarterSettingsState

router = Router()

@router.message(IsAdmin(), F.text == "⚙️ Chorak sozlamalari")
async def quarter_settings_main(message: Message):
    await message.answer("⚙️ Chorak sozlamalari bo'limiga xush kelibsiz!", reply_markup=quarter_settings_menu)

@router.message(IsAdmin(), F.text == "📊 Hozirgi chorakni ko'rish")
async def show_current_quarter(message: Message):
    quarter_settings = await QuarterSettings.first()
    
    if not quarter_settings:
        # Agar sozlamalar mavjud bo'lmasa, default yaratamiz
        quarter_settings = await QuarterSettings.create(current_quarter=1)
    
    current_quarter = quarter_settings.current_quarter
    quarter_names = {1: "1-chorak", 2: "2-chorak", 3: "3-chorak", 4: "4-chorak"}
    
    await message.answer(
        f"📊 <b>Hozirgi faol chorak:</b> {quarter_names[current_quarter]}\n\n"
        f"Yangi premium foydalanuvchilar {quarter_names[current_quarter]} taqdimotlariga ruxsat olishadi.",
        parse_mode="HTML"
    )

@router.message(IsAdmin(), F.text == "🔄 Chorakni o'zgartirish")
async def change_quarter(message: Message, state: FSMContext):
    quarter_settings = await QuarterSettings.first()
    current_quarter = quarter_settings.current_quarter if quarter_settings else 1
    
    await message.answer(
        f"🔄 Hozirgi chorak: {current_quarter}-chorak\n\n"
        "Yangi chorakni tanlang:",
        reply_markup=quarter_select_menu
    )
    await state.set_state(QuarterSettingsState.waiting_for_quarter)

@router.message(QuarterSettingsState.waiting_for_quarter, F.text.in_(["1-chorak", "2-chorak", "3-chorak", "4-chorak"]))
async def process_quarter_change(message: Message, state: FSMContext):
    quarter_number = int(message.text.split("-")[0])
    
    quarter_settings = await QuarterSettings.first()
    
    if not quarter_settings:
        quarter_settings = await QuarterSettings.create(current_quarter=quarter_number)
    else:
        quarter_settings.current_quarter = quarter_number
        await quarter_settings.save()
    
    await message.answer(
        f"✅ Chorak muvaffaqiyatli o'zgartirildi!\n\n"
        f"📊 <b>Yangi faol chorak:</b> {quarter_number}-chorak\n\n"
        f"Endi yangi premium foydalanuvchilar {quarter_number}-chorak taqdimotlariga ruxsat olishadi.",
        parse_mode="HTML",
        reply_markup=quarter_settings_menu
    )
    await state.clear()

@router.message(IsAdmin(), F.text == "⬅️ Orqaga")
async def back_to_admin_menu(message: Message, state: FSMContext):
    await message.answer("⬅️ Asosiy admin menyuga qaytdik", reply_markup=admin_main_menu)
    await state.clear()