from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.models.all_models import PresentationFiles
from filters.admins import IsAdmin
from aiogram.fsm.context import FSMContext
from states.admins import NewPresentationState, FindTaqdimotState
from keyboards.admins import taqdimotlar_menu, back_button, select_file_lang_btn, delete_taqdimot_btn

router = Router()

@router.message(IsAdmin(), F.text == "📂 Taqdimotlar")
async def f(message: Message):
    await message.answer("Taqdimotlar bo'limiga xush kelibsiz!", reply_markup=taqdimotlar_menu)

@router.message(IsAdmin(), F.text == "📂 Yangi taqdimot")
async def f(message: Message, state: FSMContext):
    await message.answer("Dars kodini kiriting:\n\nMasalan: 5-1-2", reply_markup=back_button)
    await state.set_state(NewPresentationState.waiting_for_code)

@router.message(NewPresentationState.waiting_for_code)
async def f(message: Message, state: FSMContext):
    code = message.text
    await state.update_data(code=code)
    await message.answer("Taqdimot faylini yuboring:", reply_markup=back_button)
    await state.set_state(NewPresentationState.waiting_for_file)

@router.message(NewPresentationState.waiting_for_file, F.document)
async def f(message: Message, state: FSMContext):
    file_id = message.document.file_id
    await state.update_data(file_id=file_id)
    await message.answer("Dars nomini kiriting:", reply_markup=back_button)
    await state.set_state(NewPresentationState.waiting_for_title)

@router.message(NewPresentationState.waiting_for_title)
async def f(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer("Taqdimot tilini tanlang!", reply_markup=select_file_lang_btn)
    await state.set_state(NewPresentationState.waiting_for_lang)

@router.message(NewPresentationState.waiting_for_lang)
async def f(message: Message, state: FSMContext):
    lang = message.text
    state_data = await state.get_data()
    code:str = state_data.get("code")
    title = state_data.get("title")
    file_id = state_data.get("file_id")

    await PresentationFiles.create(
        lesson_name=title,
        class_number=code.split("-")[0],
        part_number=code.split("-")[1],
        lesson_number=code.split("-")[2],
        file_lang=lang,
        file_id=file_id
    )

    await message.answer("✅ Taqdimot saqlandi!", reply_markup=taqdimotlar_menu)
    await state.clear()

@router.message(IsAdmin(), F.text == "📂 Mavjud taqdimotlar")
async def f(message: Message, state: FSMContext):
    await message.answer("Taqdimotni ko'rish uchun taqdimot kodini yuboring.\n\nMasalan: 5-1-2", reply_markup=back_button)
    await state.set_state(FindTaqdimotState.waiting_for_code)

@router.message(FindTaqdimotState.waiting_for_code)
async def f(message: Message, state: FSMContext):
    code = message.text

    presentation = await PresentationFiles.get_or_none(lesson_number=code.split("-")[0], part_number=code.split("-")[1], class_number=code.split("-")[2])
    if presentation:
        await message.answer_document(
            document=presentation.file_id,
            caption=f"""
Dars nomi: {presentation.lesson_name}
Taqdimot tili: {presentation.file_lang}
Qo'shilgan sana: {presentation.created_at.date()}
            """,
            reply_markup=delete_taqdimot_btn(presentation.id)
        )
    else:
        await message.answer("❌ Taqdimot topilmadi!", reply_markup=taqdimotlar_menu)

@router.callback_query(F.data.startswith("delete-taqdimot_"))
async def f(callback: CallbackQuery, state: FSMContext):
    taqdimot_id = callback.data.split("_")[1]
    try: await PresentationFiles.filter(id=taqdimot_id).delete()
    except: await callback.answer("❌ Taqdimot topilmadi!", show_alert=True)
    else: await callback.answer("✅ Taqdimot o'chirildi!", show_alert=True)