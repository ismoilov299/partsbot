"""
Usta Xona add handlers - service center registration
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_cancel_keyboard, get_phone_keyboard, Texts
from bot.utils import database as db
from bot.states import UstaXonaAddStates

router = Router()


@router.callback_query(F.data == "usta_xona_add")
async def usta_xona_add_start(callback: CallbackQuery, state: FSMContext):
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "Usta xona qo'shish\n\nUsta xona nomini kiriting:"
    else:
        text = "Dobavlenie servisa\n\nVvedite nazvanie servisa:"
    
    await callback.message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.enter_service_name)
    await callback.answer()


@router.message(UstaXonaAddStates.enter_service_name)
async def process_service_name(message: Message, state: FSMContext):
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "Bekor qilindi" if user.language == 'uz' else "Otmeneno"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(service_name=message.text)
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "Telefon raqamingizni kiriting yoki tugmani bosing:\n\nMasalan: +998901234567"
    else:
        text = "Vvedite nomer telefona ili nazhmite knopku:\n\nNaprimer: +998901234567"
    
    await message.answer(text, reply_markup=get_phone_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.enter_phone)


@router.message(UstaXonaAddStates.enter_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    
    data = await state.get_data()
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = f"Ma'lumotlar qabul qilindi!\n\nNomi: {data['service_name']}\nTelefon: {phone}\n\nAdmin tasdiqlaydi."
    else:
        text = f"Dannye prinyaty!\n\nNazvanie: {data['service_name']}\nTelefon: {phone}\n\nAdmin podtverdit."
    
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    
    from bot.keyboards.inline import get_main_menu_keyboard
    menu_text = "Asosiy menyu:" if user.language == 'uz' else "Glavnoe menyu:"
    await message.answer(menu_text, reply_markup=get_main_menu_keyboard(user.language))
    await state.clear()


@router.message(UstaXonaAddStates.enter_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "Bekor qilindi" if user.language == 'uz' else "Otmeneno"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    phone = message.text.strip()
    if not phone.startswith('+'):
        phone = '+' + phone
    
    data = await state.get_data()
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = f"Ma'lumotlar qabul qilindi!\n\nNomi: {data['service_name']}\nTelefon: {phone}\n\nAdmin tasdiqlaydi."
    else:
        text = f"Dannye prinyaty!\n\nNazvanie: {data['service_name']}\nTelefon: {phone}\n\nAdmin podtverdit."
    
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    
    from bot.keyboards.inline import get_main_menu_keyboard
    menu_text = "Asosiy menyu:" if user.language == 'uz' else "Glavnoe menyu:"
    await message.answer(menu_text, reply_markup=get_main_menu_keyboard(user.language))
    await state.clear()
