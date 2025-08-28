from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.models.all_models import User
from keyboards.admins import back_button, confirm_payment_btn
from config import CARD_NUMBER, CARD_OWNER, SUBSCRIPTION_PRICE, ADMIN
from states.users import SubscriptionState

router = Router()

@router.message(F.text == "Obuna harid qilish")
async def f(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user.is_premium:
        await message.answer("Siz allaqachon obuna harid qilgansiz.")
        return
    
    await message.answer(
        text=f"""
💳 <b>Obuna harid qilish uchun quyidagi kartaga {SUBSCRIPTION_PRICE} so'm to'lov qilib, screanshootini shu yerga yuboring.</b>

<b>Karta raqami:</b> <code>{CARD_NUMBER}</code>
<b>Karta egasi:</b> <i>{CARD_OWNER}</i>
""",
        parse_mode="HTML",
        reply_markup=back_button
    )
    await state.set_state(SubscriptionState.waiting_for_payment)

@router.message(SubscriptionState.waiting_for_payment, F.photo)
async def f(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user.is_premium:
        await message.answer("Siz allaqachon obuna harid qilgansiz.")
        return
    await message.bot.send_photo(
        chat_id=ADMIN,
        photo=message.photo[-1].file_id,
        caption=f"""
YANGI OBUNA SO'ROVI:

<b>Foydalanuvchi:</b> {user.name}
<b>To'lov miqdori:</b> {SUBSCRIPTION_PRICE} so'm
""",
        parse_mode="HTML",
        reply_markup=confirm_payment_btn(message.from_user.id)
    )
