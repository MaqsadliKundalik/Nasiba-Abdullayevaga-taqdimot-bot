from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.models.all_models import User, QuarterSettings, UserQuarterSubscription
from keyboards.admins import back_button, confirm_quarter_payment_btn
from config import CARD_NUMBER, CARD_OWNER, QUARTER_PRICE, ADMIN
from states.users import QuarterSubscriptionState

router = Router()

@router.message(F.text == "Obuna harid qilish")
async def subscription_purchase(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    
    # To'liq premium tekshir
    if user.is_premium:
        await message.answer("✅ Siz allaqachon barcha choraklar uchun obuna harid qilgansiz!")
        return
    
    # Hozirgi chorakni ol
    quarter_settings = await QuarterSettings.first()
    current_quarter = quarter_settings.current_quarter if quarter_settings else 1
    
    # Hozirgi chorak uchun obuna bor yoki yo'qligini tekshir
    current_subscription = await UserQuarterSubscription.get_or_none(
        user=user, 
        quarter_number=current_quarter, 
        is_active=True
    )
    
    if current_subscription:
        await message.answer(f"✅ Siz {current_quarter}-chorak uchun allaqachon obuna harid qilgansiz!")
        return
    
    await message.answer(
        text=f"""
💳 <b>{current_quarter}-chorak obunasi uchun quyidagi kartaga {QUARTER_PRICE:,} so'm to'lov qilib, screanshootini shu yerga yuboring.</b>

<b>Karta raqami:</b> <code>{CARD_NUMBER}</code>
<b>Karta egasi:</b> <i>{CARD_OWNER}</i>

📚 <b>Hozirgi chorak:</b> {current_quarter}-chorak
💰 <b>Narx:</b> {QUARTER_PRICE:,} so'm
""",
        parse_mode="HTML",
        reply_markup=back_button
    )
    await state.update_data(quarter_number=current_quarter)
    await state.set_state(QuarterSubscriptionState.waiting_for_payment)

@router.message(F.text.regexp(r"🆕 \d+-chorak sotib olish"))
async def new_quarter_purchase(message: Message, state: FSMContext):
    # Chorak raqamini ajratib olish
    quarter_number = int(message.text.split()[1].split("-")[0])
    
    user = await User.get_or_none(tg_id=message.from_user.id)
    
    # To'liq premium tekshir
    if user.is_premium:
        await message.answer("✅ Siz allaqachon barcha choraklar uchun obuna harid qilgansiz!")
        return
    
    # Bu chorak uchun obuna bor yoki yo'qligini tekshir
    existing_subscription = await UserQuarterSubscription.get_or_none(
        user=user, 
        quarter_number=quarter_number, 
        is_active=True
    )
    
    if existing_subscription:
        await message.answer(f"✅ Siz {quarter_number}-chorak uchun allaqachon obuna harid qilgansiz!")
        return
    
    await message.answer(
        text=f"""
💳 <b>{quarter_number}-chorak obunasi uchun quyidagi kartaga {QUARTER_PRICE:,} so'm to'lov qilib, screanshootini shu yerga yuboring.</b>

<b>Karta raqami:</b> <code>{CARD_NUMBER}</code>
<b>Karta egasi:</b> <i>{CARD_OWNER}</i>

📚 <b>Chorak:</b> {quarter_number}-chorak
💰 <b>Narx:</b> {QUARTER_PRICE:,} so'm
""",
        parse_mode="HTML",
        reply_markup=back_button
    )
    await state.update_data(quarter_number=quarter_number)
    await state.set_state(QuarterSubscriptionState.waiting_for_payment)

@router.message(QuarterSubscriptionState.waiting_for_payment, F.photo)
async def process_quarter_payment(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    state_data = await state.get_data()
    quarter_number = state_data.get('quarter_number')
    
    # Qaytadan tekshir: bu chorakni oldin sotib olgani yo'qmi
    existing_subscription = await UserQuarterSubscription.get_or_none(
        user=user, quarter_number=quarter_number, is_active=True
    )
    
    if existing_subscription:
        await message.answer("Siz bu chorak uchun allaqachon obuna harid qilgansiz!")
        await state.clear()
        return
    
    await message.bot.send_photo(
        chat_id=ADMIN,
        photo=message.photo[-1].file_id,
        caption=f"""
YANGI CHORAK OBUNA SO'ROVI:

<b>Foydalanuvchi:</b> {user.name}
<b>To'lov miqdori:</b> {QUARTER_PRICE:,} so'm
<b>Obuna turi:</b> {quarter_number}-chorak obunasi
""",
        parse_mode="HTML",
        reply_markup=confirm_quarter_payment_btn(message.from_user.id, quarter_number)
    )
    await message.answer("📸 Screanshot qabul qilindi! Admin tekshiruvdan so'ng obuna faollashtiriladi.")
    await state.clear()
