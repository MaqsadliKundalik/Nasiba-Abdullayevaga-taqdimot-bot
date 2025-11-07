from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_users_menu = ReplyKeyboardBuilder()
main_users_menu.button(text="Obuna harid qilish")
main_users_menu.button(text="Mening profilim")
main_users_menu.button(text="Yordam")
main_users_menu.adjust(1)
main_users_menu = main_users_menu.as_markup(resize_keyboard=True)

main_menu_prem_users = ReplyKeyboardBuilder()
main_menu_prem_users.button(text="Taqdimot qidirish")
main_menu_prem_users.button(text="Mening profilim")
main_menu_prem_users.button(text="Yordam")
main_menu_prem_users.adjust(1)
main_menu_prem_users = main_menu_prem_users.as_markup(resize_keyboard=True)

def create_new_quarter_menu(quarter_number):
    """Yangi chorak uchun klaviatura yaratish"""
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Taqdimot qidirish")
    keyboard.button(text=f"🆕 {quarter_number}-chorak sotib olish")
    keyboard.button(text="Mening profilim")
    keyboard.button(text="Yordam")
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
