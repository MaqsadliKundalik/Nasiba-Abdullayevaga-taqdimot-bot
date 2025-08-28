from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models.all_models import User
from states.users import HelpState
from config import ADMIN
from keyboards.admins import back_button, aks_help_btn
from keyboards.users import main_users_menu, main_menu_prem_users

router = Router()

@router.message(F.text == "Mening profilim")
async def f(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user:
        await message.answer(f"👤 Sizning profilingiz:\n\n"
                             f"Ism: {user.name}\n"
                             f"Telefon: {user.phone_number}\n"
                             f"Obuna: {'✅' if user.is_premium else '❌'}\n"
                             f"Ro'yxatdan o'tilgan sana: {user.created_at.date()}")
    else:
        await message.answer("❌ Profil topilmadi!")

@router.message(F.text == "Yordam")
async def f(message: Message, state: FSMContext):
    await message.answer("📚 Yordam bo'limiga xush kelibsiz!\n\n"
                         "Sizga qanday yordam bera olishim mumkin? (Hammasini bitta xabrda yozing)", reply_markup=back_button)
    await state.set_state(HelpState.waiting_for_msg)

@router.message(HelpState.waiting_for_msg)
async def f(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    await message.copy_to(ADMIN)
    await message.bot.send_message(ADMIN, f"Yordam so'rovi:\n\nIsm: {user.name}\nTelefon raqam: {user.phone_number}", reply_markup=aks_help_btn(user.tg_id))
    if user.is_premium: await message.answer("✅ Sizning xabaringiz yuborildi!", reply_markup=main_menu_prem_users)
    else: await message.answer("✅ Sizning xabaringiz yuborildi!", reply_markup=main_users_menu)