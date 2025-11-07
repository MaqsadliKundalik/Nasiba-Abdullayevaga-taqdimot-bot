from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import QUARTER_PRICE
from database.models.all_models import User, UserQuarterSubscription
from filters.admins import IsAdmin
from keyboards.users import main_menu_prem_users

router = Router()

@router.callback_query(IsAdmin(), F.data.startswith("confirm-quarter-payment"))
async def confirm_quarter_payment(callback: CallbackQuery, state: FSMContext):
    # callback_data format: "confirm-quarter-payment_user_id_quarter_number"
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("Noto'g'ri callback data format!", show_alert=True)
        return
        
    user_id = parts[1]
    quarter_number = int(parts[2])
    
    user = await User.get_or_none(tg_id=user_id)
    if user:
        # Tekshir: bu chorakni oldin sotib olgani yo'qmi
        existing_subscription = await UserQuarterSubscription.get_or_none(
            user=user, quarter_number=quarter_number, is_active=True
        )
        
        if existing_subscription:
            await callback.answer("Bu foydalanuvchi bu chorak uchun allaqachon obuna harid qilgan!", show_alert=True)
            return
        
        # Yangi chorak obunasini yarat
        await UserQuarterSubscription.create(
            user=user,
            quarter_number=quarter_number,
            is_active=True
        )
        
        await callback.bot.send_message(
            chat_id=user.tg_id,
            text=f"✅ {quarter_number}-chorak obunangiz muvaffaqiyatli tasdiqlandi!",
            reply_markup=main_menu_prem_users
        )
        
        await callback.message.edit_caption(
            caption=f"""
YANGI CHORAK OBUNA SO'ROVI:

<b>Foydalanuvchi:</b> {user.name}
<b>To'lov miqdori:</b> {QUARTER_PRICE:,} so'm
<b>Obuna turi:</b> {quarter_number}-chorak obunasi

✅ {quarter_number}-chorak obuna muvaffaqiyatli tasdiqlandi.
                                            """,
                                            parse_mode="HTML"
        )
        await callback.answer(f"{quarter_number}-chorak obuna muvaffaqiyatli tasdiqlandi.")
    else:
        await callback.answer("Foydalanuvchi topilmadi.")

@router.callback_query(IsAdmin(), F.data.startswith("reject-quarter-payment"))
async def reject_quarter_payment(callback: CallbackQuery, state: FSMContext):
    # callback_data format: "reject-quarter-payment_user_id_quarter_number"
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("Noto'g'ri callback data format!", show_alert=True)
        return
        
    user_id = parts[1]
    quarter_number = int(parts[2])
    
    user = await User.get_or_none(tg_id=user_id)
    if user:
        await callback.bot.send_message(
            chat_id=user.tg_id,
            text=f"❌ {quarter_number}-chorak obuna to'lovingiz rad etildi. Iltimos, qayta urinib ko'ring yoki yordam uchun admin bilan bog'laning."
        )
        await callback.message.edit_caption(
            caption=f"""
YANGI CHORAK OBUNA SO'ROVI:

<b>Foydalanuvchi:</b> {user.name}
<b>To'lov miqdori:</b> {QUARTER_PRICE:,} so'm
<b>Obuna turi:</b> {quarter_number}-chorak obunasi

❌ {quarter_number}-chorak obuna rad etildi.
                                            """,
                                            parse_mode="HTML"
        )
        await callback.answer(f"{quarter_number}-chorak obuna rad etildi.")
    else:
        await callback.answer("Foydalanuvchi topilmadi.")