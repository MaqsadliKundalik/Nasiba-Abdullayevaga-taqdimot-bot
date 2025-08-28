from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from database.models.all_models import User
import pandas as pd
from keyboards.admins import users_menu

router = Router()

@router.message(F.text == "👤 Foydalanuvchilar")
async def f(message: Message):
    await message.answer("Qaysi ro'yhatni olmoqchisiz?", reply_markup=users_menu)

@router.message(F.text == "👑 Premium foydalanuvchilar ro'yxati")
async def show_users(message: Message):
    users = await User.all()
    data = [{"ID": user.id, "Ism": user.name, "Telefom raqam": user.phone_number, "Qo'shilgan vaqti": user.created_at} for user in users if user.is_premium]
    df = pd.DataFrame(data)

    file_path = "hisobot.xlsx"
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Users")

    await message.answer_document(document=FSInputFile(file_path), caption="👑 Premium foydalanuvchilar ro'yxati")

@router.message(F.text == "👤 Barcha Foydalanuvchilar ro'yxati")
async def show_all_users(message: Message):
    users = await User.all()
    data = [{"ID": user.id, "Ism": user.name, "Telefom raqam": user.phone_number, "Qo'shilgan vaqti": user.created_at} for user in users]
    df = pd.DataFrame(data)

    file_path = "hisobot_barcha.xlsx"
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Users")

    await message.answer_document(document=FSInputFile(file_path), caption="👤 Barcha Foydalanuvchilar ro'yxati")
