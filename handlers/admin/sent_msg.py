from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models.all_models import User
from states.admins import SentMsgState
from asyncio import sleep
from keyboards.admins import admin_main_menu, back_button

router = Router()

@router.message(F.text == "✉️ Xabar yuborish")
async def process_send_message(message: Message, state: FSMContext):
    await state.set_state(SentMsgState.waiting_for_message)
    await message.answer("Xabarni yuboring.", reply_markup=back_button)

@router.message(SentMsgState.waiting_for_message)
async def process_waiting_for_message(message: Message, state: FSMContext):
    users = await User.all()
    count = 0
    msg = await message.answer("Xabar yuborishn boshladim....")
    for user in users:
        try:
            await message.copy_to(chat_id=user.tg_id)
            count += 1
            await msg.edit_text(f"Hozirda xabar {count} ta foydalanuvchiga yuborildi...")
            await sleep(0.5)
        except Exception as e:
            print(f"Failed to send message to {user.tg_id}: {e}")
    await msg.edit_text(f"Xabar {count} ta foydalanuvchiga yuborildi.")
    await message.answer("Jarayon yakunlandi.", reply_markup=admin_main_menu)
    await state.clear()