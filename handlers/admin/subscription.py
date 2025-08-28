from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import SUBSCRIPTION_PRICE
from database.models.all_models import User
from filters.admins import IsAdmin
from keyboards.users import main_menu_prem_users

router = Router()

@router.callback_query(IsAdmin(), F.data.startswith("confirm-payment"))
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("_")[1]
    user = await User.get_or_none(tg_id=user_id)
    if user:
        user.is_premium = True
        await user.save()
        await callback.bot.send_message(
            chat_id=user.tg_id,
            text="✅ To'lovingiz muvaffaqiyatli tasdiqlandi.",
            reply_markup=main_menu_prem_users
        )
        await callback.message.edit_caption(
            caption=f"""
YANGI OBUNA SO'ROVI:

<b>Foydalanuvchi:</b> {user.name}
<b>To'lov miqdori:</b> {SUBSCRIPTION_PRICE} so'm

✅ Obuna muvaffaqiyatli tasdiqlandi.
                                            """,
                                            parse_mode="HTML"
        )
        await callback.answer("Obuna muvaffaqiyatli tasdiqlandi.")
    else:
        await callback.answer("Foydalanuvchi topilmadi.")
