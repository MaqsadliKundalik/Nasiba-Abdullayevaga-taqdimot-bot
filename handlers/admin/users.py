from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from database.models.all_models import User
from keyboards.admins import users_menu
import pandas as pd
from io import BytesIO

router = Router()

@router.message(F.text == "👤 Foydalanuvchilar")
async def f(message: Message):
    await message.answer("Qaysi ro'yxatni olmoqchisiz?", reply_markup=users_menu)

async def _build_users_excel(queryset, filename: str, caption: str):
    rows = await queryset.values("id", "tg_id", "name", "phone_number", "created_at")

    df = pd.DataFrame([
        {
            "ID (PK)": r["id"],
            "Telegram ID": r["tg_id"],
            "Ism": r["name"],
            "Telefon raqam": r["phone_number"],
            "Qo'shilgan vaqti": r["created_at"],
        } for r in rows
    ])

    if not df.empty:
        df["Qo'shilgan vaqti"] = pd.to_datetime(
            df["Qo'shilgan vaqti"], errors="coerce", utc=True
        ).dt.tz_localize(None)

    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="xlsxwriter", datetime_format="yyyy-mm-dd hh:mm:ss") as writer:
        df.to_excel(writer, index=False, sheet_name="Users")
    bio.seek(0)

    doc = BufferedInputFile(bio.read(), filename=filename)
    return doc, caption

@router.message(F.text == "👑 Premium foydalanuvchilar ro'yxati")
async def show_premium_users(message: Message):
    queryset = User.filter(is_premium=True).order_by("id")
    doc, cap = await _build_users_excel(
        queryset,
        filename="premium_foydalanuvchilar.xlsx",
        caption="👑 Premium foydalanuvchilar ro'yxati"
    )
    await message.answer_document(document=doc, caption=cap)

@router.message(F.text == "👤 Barcha Foydalanuvchilar ro'yxati")
async def show_all_users(message: Message):
    queryset = User.all().order_by("id")
    doc, cap = await _build_users_excel(
        queryset,
        filename="barcha_foydalanuvchilar.xlsx",
        caption="👤 Barcha foydalanuvchilar ro'yxati"
    )
    await message.answer_document(document=doc, caption=cap)
