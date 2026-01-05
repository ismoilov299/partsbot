"""
Leave request handlers - full implementation
"""
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_cancel_keyboard, get_phone_keyboard, Texts
from bot.utils import db
from bot.states import RequestStates

router = Router()


@router.callback_query(F.data == "leave_request")
async def leave_request_start(callback: CallbackQuery, state: FSMContext):
    """Start request leaving process - ask for description"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "📝 So'rov qoldirish\n\n"
        text += "Iltimos, qidrayotgan ehtiyot qismingiz haqida to'liq ma'lumot yozing:\n"
        text += "• Avtomobil markasi va modeli\n"
        text += "• Yili\n"
        text += "• Qaysi ehtiyot qism kerak\n\n"
        text += "Masalan: Cobalt 2, 2014 yil, old faralar"
    else:
        text = "📝 Оставить запрос\n\n"
        text += "Пожалуйста, пропишите модель, год и название запчасти которую вы ищете:\n\n"
        text += "Например: Cobalt 2, 2014 год, передние фары"
    
    await callback.message.answer(
        text,
        reply_markup=get_cancel_keyboard(user.language)
    )
    await state.set_state(RequestStates.enter_description)
    await callback.answer()


@router.message(RequestStates.enter_description)
async def process_request_description(message: Message, state: FSMContext):
    """Process request description and check if phone needed"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    # Save description to state
    await state.update_data(description=message.text)
    user = await db.get_user(message.from_user.id)
    
    # Check if user has username
    if user.username:
        # User has username, create request directly
        await create_and_send_request(message, state, user, message.text, None)
    else:
        # User doesn't have username, ask for phone
        if user.language == 'uz':
            text = "📞 Siz bilan bog'lanish uchun telefon raqamingizni kiriting yoki tugmani bosing:\n\n"
            text += "Masalan: +998901234567\n"
            text += "Yoki 📱 tugmasini bosing"
        else:
            text = "📞 Введите номер телефона для связи с вами или нажмите кнопку:\n\n"
            text += "Например: +998901234567\n"
            text += "Или нажмите кнопку 📱"
        
        await message.answer(text, reply_markup=get_phone_keyboard(user.language))
        await state.set_state(RequestStates.enter_phone)


@router.message(RequestStates.enter_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone via contact button"""
    phone = message.contact.phone_number
    
    # Format phone number
    if not phone.startswith('+'):
        phone = '+' + phone
    
    # Get saved description from state
    data = await state.get_data()
    description = data.get('description')
    user = await db.get_user(message.from_user.id)
    
    await create_and_send_request(message, state, user, description, phone)


@router.message(RequestStates.enter_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    """Process phone as text input"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    phone = message.text.strip()
    
    # Get saved description from state
    data = await state.get_data()
    description = data.get('description')
    user = await db.get_user(message.from_user.id)
    
    await create_and_send_request(message, state, user, description, phone)


async def create_and_send_request(message: Message, state: FSMContext, user, description: str, phone: str):
    """Create request and send to admin"""
    # Save request to database
    try:
        request = await db.create_request(
            user_id=message.from_user.id,
            description=description,
            phone=phone
        )
        
        # Send confirmation to user
        if user.language == 'uz':
            confirmation_text = "✅ So'rovingiz qabul qilindi!\n\n"
            confirmation_text += "Tez orada siz bilan bog'lanamiz.\n\n"
            confirmation_text += f"So'rov raqami: #{request.id}"
        else:
            confirmation_text = "✅ Ваш запрос принят!\n\n"
            confirmation_text += "Скоро с вами свяжутся.\n\n"
            confirmation_text += f"Номер запроса: #{request.id}"
        
        await message.answer(confirmation_text, reply_markup=ReplyKeyboardRemove())
        
        # Forward request to admin and group
        admin_chat_id = os.getenv('ADMIN_CHAT_ID')
        group_chat_id = os.getenv('GROUP_CHAT_ID', '-1003392656006')
        
        if admin_chat_id or group_chat_id:
            try:
                # Create admin message
                admin_text = "🔔 YANGI SO'ROV\n\n"
                admin_text += f"👤 Kimdan: {user.first_name}"
                if user.username:
                    admin_text += f" (@{user.username})"
                else:
                    admin_text += f" (Username yo'q)"
                admin_text += f"\n📱 ID: {user.telegram_id}"
                if phone:
                    admin_text += f"\n📞 Telefon: {phone}"
                admin_text += f"\n\n📝 So'rov:\n{description}"
                admin_text += f"\n\n#sorov_{request.id}"
                
                # Send to admin and group
                from aiogram import Bot
                bot = Bot(token=os.getenv('BOT_TOKEN'))
                
                if admin_chat_id:
                    await bot.send_message(
                        chat_id=admin_chat_id,
                        text=admin_text
                    )
                
                if group_chat_id:
                    await bot.send_message(
                        chat_id=group_chat_id,
                        text=admin_text
                    )
                
            except Exception as e:
                print(f"Error sending to admin: {e}")
        
    except Exception as e:
        if user.language == 'uz':
            error_text = f"❌ Xatolik yuz berdi: {str(e)}\n\nIltimos, qayta urinib ko'ring."
        else:
            error_text = f"❌ Произошла ошибка: {str(e)}\n\nПожалуйста, попробуйте снова."
        
        await message.answer(error_text)
    
    await state.clear()
