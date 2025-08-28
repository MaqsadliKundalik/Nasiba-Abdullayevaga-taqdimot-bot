from aiogram import Router, F
from filters.users import IsNewUser
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database.models.all_models import User
from states.users import UserRegisterSState
from keyboards.users import main_users_menu, main_menu_prem_users
import re

router = Router()

@router.message(UserRegisterSState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone_pattern = re.compile(r"^\+998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$")
    if phone_pattern.match(message.text):
        phone_number = re.sub(r"\s+", "", message.text)  # Remove spaces
        await message.answer(f"Telefon raqamingiz qabul qilindi: {phone_number}\n\nEndi ismingizni yuboring.")
        await state.update_data(phone=phone_number)
        await state.set_state(UserRegisterSState.waiting_for_name)
    else:
        await message.answer("Telefon raqami noto'g'ri formatda. Iltimos, quyidagicha yuboring:\n\n"
                             "+998 91 234 56 78")

@router.message(UserRegisterSState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if name and len(name) <= 200:
        await message.answer(f"Ismingiz qabul qilindi: {name}")

        state_data = await state.get_data()
        phone_number = state_data.get("phone")
        await User.create(phone_number=phone_number, name=name, tg_id=message.from_user.id)
        await state.clear()
        await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz! 🎉", reply_markup=main_users_menu)
    else:
        await message.answer("Iltimos, ismingizni yuboring.")   

@router.message(IsNewUser())
async def new_user_handler(message: Message, state: FSMContext):
    await message.answer("Xush kelibsiz 😊")
    await message.answer("Menga telefon raqamingizni yuboring.\n\nNa'muna: +998 90 123 45 67")
    await state.set_state(UserRegisterSState.waiting_for_phone)

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user.is_premium:
        await message.answer("Xush kelibsiz! 😊", reply_markup=main_menu_prem_users)
    else:
        await message.answer("Xush kelibsiz! 😊", reply_markup=main_users_menu)

@router.message(F.text == "⬅️ Orqaga")
async def back_to_main_menu(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user.is_premium:
        await message.answer("⬅️ Asosiy menyuga qaytdik", reply_markup=main_menu_prem_users)
    else: 
        await message.answer("⬅️ Asosiy menyuga qaytdik", reply_markup=main_users_menu)
    await state.clear()