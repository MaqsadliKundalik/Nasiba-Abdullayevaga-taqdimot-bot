from aiogram import Router, F
from aiogram.types import Message
from filters.admins import IsAdmin
from aiogram.filters import CommandStart
from keyboards.admins import admin_main_menu
from aiogram.fsm.context import FSMContext

router = Router()
@router.message(IsAdmin(), CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Xush kelibsiz 😊", reply_markup=admin_main_menu)
    await state.clear()

@router.message(IsAdmin(), F.text == "⬅️ Orqaga")
async def back_to_main_menu(message: Message, state: FSMContext):
    await message.answer("⬅️ Asosiy menyuga qaytdik", reply_markup=admin_main_menu)
    await state.clear()