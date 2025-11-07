from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

admin_main_menu = ReplyKeyboardBuilder()
admin_main_menu.button(text="👤 Foydalanuvchilar")
admin_main_menu.button(text="📂 Taqdimotlar")
admin_main_menu.button(text="⚙️ Chorak sozlamalari")
admin_main_menu.button(text="✉️ Xabar yuborish")
admin_main_menu.adjust(2)
admin_main_menu = admin_main_menu.as_markup(resize_keyboard=True)

users_menu = ReplyKeyboardBuilder()
users_menu.button(text="👤 Barcha Foydalanuvchilar ro'yxati")
users_menu.button(text="👑 Premium foydalanuvchilar ro'yxati")
users_menu.button(text="⬅️ Orqaga")
users_menu.adjust(1)
users_menu = users_menu.as_markup(resize_keyboard=True)

taqdimotlar_menu = ReplyKeyboardBuilder()
taqdimotlar_menu.button(text="📂 Yangi taqdimot")
taqdimotlar_menu.button(text="📂 Mavjud taqdimotlar")
taqdimotlar_menu.button(text="⬅️ Orqaga")
taqdimotlar_menu.adjust(2)
taqdimotlar_menu = taqdimotlar_menu.as_markup(resize_keyboard=True)

back_button = ReplyKeyboardBuilder()
back_button.button(text="⬅️ Orqaga")
back_button = back_button.as_markup(resize_keyboard=True)

select_file_lang_btn = ReplyKeyboardBuilder()
select_file_lang_btn.button(text="O'zbekcha")
select_file_lang_btn.button(text="Русский")
select_file_lang_btn = select_file_lang_btn.as_markup(resize_keyboard=True)

def delete_taqdimot_btn(taqdimot_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🗑️ Taqdimotni o'chirish", callback_data=f"delete-taqdimot_{taqdimot_id}")
    return keyboard.as_markup()

def aks_help_btn(user_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Javob berish", callback_data=f"help_{user_id}")
    return keyboard.as_markup()

quarter_settings_menu = ReplyKeyboardBuilder()
quarter_settings_menu.button(text="📊 Hozirgi chorakni ko'rish")
quarter_settings_menu.button(text="🔄 Chorakni o'zgartirish")
quarter_settings_menu.button(text="⬅️ Orqaga")
quarter_settings_menu.adjust(1)
quarter_settings_menu = quarter_settings_menu.as_markup(resize_keyboard=True)

quarter_select_menu = ReplyKeyboardBuilder()
quarter_select_menu.button(text="1-chorak")
quarter_select_menu.button(text="2-chorak")
quarter_select_menu.button(text="3-chorak")
quarter_select_menu.button(text="4-chorak")
quarter_select_menu.button(text="⬅️ Orqaga")
quarter_select_menu.adjust(2)
quarter_select_menu = quarter_select_menu.as_markup(resize_keyboard=True)

def confirm_quarter_payment_btn(user_id, quarter_number):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ To'lovni tasdiqlash", callback_data=f"confirm-quarter-payment_{user_id}_{quarter_number}")
    keyboard.button(text="❌ To'lovni rad etish", callback_data=f"reject-quarter-payment_{user_id}_{quarter_number}")
    keyboard.adjust(1)
    return keyboard.as_markup()