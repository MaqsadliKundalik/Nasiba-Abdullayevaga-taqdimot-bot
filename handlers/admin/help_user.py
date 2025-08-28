from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.models.all_models import User
from aiogram.fsm.context import FSMContext
from states.admins import HelpAdminState

router = Router()

@router.callback_query(F.data.startswith("help_"))
async def f(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("_")[1]
    user = await User.get_or_none(tg_id=user_id)
    if user:
        await callback.message.edit_text(
            text=f"""
Yordam so'rovi:
Ism: {user.name}
Telefon raqam: {user.phone_number}

Javobingizni yuboring.
            """,
        )
        await state.update_data(user_id=user_id)
        await state.set_state(HelpAdminState.waiting_for_msg)

@router.message(HelpAdminState.waiting_for_msg)
async def f(message: Message, state: FSMContext):
    statedata = await state.get_data()
    user_id = statedata.get("user_id")
    user = await User.get_or_none(tg_id=user_id)
    if user:
        await message.bot.send_message(user.tg_id, "✅ Sizning xabaringizga javob berildi.")
        await message.copy_to(user.tg_id)
        await message.answer("✅ Sizning xabaringiz yuborildi!")