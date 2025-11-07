from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings
from states.users import HelpState
from config import ADMIN
from keyboards.admins import back_button, aks_help_btn
from keyboards.users import main_users_menu, main_menu_prem_users

router = Router()

@router.message(F.text == "Mening profilim")
async def show_profile(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user:
        # Chorak obunalarini ol
        quarter_subscriptions = await UserQuarterSubscription.filter(user=user, is_active=True).all()
        
        profile_text = f"👤 <b>Sizning profilingiz:</b>\n\n"
        profile_text += f"📝 <b>Ism:</b> {user.name}\n"
        profile_text += f"📱 <b>Telefon:</b> {user.phone_number}\n"
        profile_text += f"📅 <b>Ro'yxatdan o'tilgan:</b> {user.created_at.date()}\n\n"
        
        # Obuna ma'lumotlari
        profile_text += f"💎 <b>Obuna holati:</b>\n"
        
        if quarter_subscriptions:
            if user.is_premium:
                profile_text += f"📚 Premium obunalar:\n"
            else:
                profile_text += f"📚 Chorak obunalari:\n"
            for sub in sorted(quarter_subscriptions, key=lambda x: x.quarter_number):
                profile_text += f"   ✅ {sub.quarter_number}-chorak\n"
        else:
            profile_text += f"❌ Obuna mavjud emas\n"
        
        await message.answer(profile_text, parse_mode="HTML")
    else:
        await message.answer("❌ Profil topilmadi!")

@router.message(F.text == "Yordam")
async def help_request(message: Message, state: FSMContext):
    await message.answer("📚 Yordam bo'limiga xush kelibsiz!\n\n"
                         "Sizga qanday yordam bera olishim mumkin? (Hammasini bitta xabrda yozing)", reply_markup=back_button)
    await state.set_state(HelpState.waiting_for_msg)

@router.message(HelpState.waiting_for_msg)
async def process_help_message(message: Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    await message.copy_to(ADMIN)
    await message.bot.send_message(ADMIN, f"Yordam so'rovi:\n\nIsm: {user.name}\nTelefon raqam: {user.phone_number}", reply_markup=aks_help_btn(user.tg_id))
    
    # Hozirgi chorakni ol
    quarter_settings = await QuarterSettings.first()
    current_quarter = quarter_settings.current_quarter if quarter_settings else 1
    
    # Foydalanuvchining obuna holatini aniqlash
    if user.is_premium:
        await message.answer("✅ Sizning xabaringiz yuborildi!", reply_markup=main_menu_prem_users)
    else:
        quarter_subscriptions = await UserQuarterSubscription.filter(user=user, is_active=True).all()
        user_quarter_numbers = [sub.quarter_number for sub in quarter_subscriptions]
        
        if quarter_subscriptions:
            # Hozirgi chorak uchun obuna bor yoki yo'qligini tekshir
            has_current_quarter = current_quarter in user_quarter_numbers
            
            if has_current_quarter:
                await message.answer("✅ Sizning xabaringiz yuborildi!", reply_markup=main_menu_prem_users)
            else:
                # Yangi chorak tugmasini ko'rsatish
                from keyboards.users import create_new_quarter_menu
                await message.answer("✅ Sizning xabaringiz yuborildi!", reply_markup=create_new_quarter_menu(current_quarter))
        else:
            await message.answer("✅ Sizning xabaringiz yuborildi!", reply_markup=main_users_menu)
    await state.clear()