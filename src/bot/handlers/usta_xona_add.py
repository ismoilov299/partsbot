"""
Usta Xona add handlers - service center registration
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.keyboards import (
    get_cancel_keyboard, get_phone_keyboard, get_location_keyboard,
    get_cities_keyboard, get_car_brands_keyboard, Texts
)
from bot.keyboards.inline import get_main_menu_keyboard
from bot.utils import database as db
from bot.states import UstaXonaAddStates

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "usta_xona_add")
async def usta_xona_add_start(callback: CallbackQuery, state: FSMContext):
    """Start usta xona registration process"""
    logger.info(f"User {callback.from_user.id} started usta xona registration")
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "🔧 Usta xona qo'shish\n\n1️⃣ Usta xona nomini kiriting:"
    else:
        text = "🔧 Добавление сервиса\n\n1️⃣ Введите название сервиса:"
    
    await callback.message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.enter_service_name)
    await callback.answer()


@router.message(UstaXonaAddStates.enter_service_name)
async def process_service_name(message: Message, state: FSMContext):
    """Process service name input"""
    logger.info(f"User {message.from_user.id} entered service name: {message.text}")
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "❌ Bekor qilindi" if user.language == 'uz' else "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(service_name=message.text)
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "2️⃣ Telefon raqamingizni kiriting yoki tugmani bosing:\n\nMasalan: +998901234567"
    else:
        text = "2️⃣ Введите номер телефона или нажмите кнопку:\n\nНапример: +998901234567"
    
    await message.answer(text, reply_markup=get_phone_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.enter_phone)


@router.message(UstaXonaAddStates.enter_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone number from contact"""
    logger.info(f"User {message.from_user.id} shared contact")
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    
    await state.update_data(phone=phone)
    user = await db.get_user(message.from_user.id)
    
    # Get cities for selection
    cities = await db.get_all_cities()
    
    if user.language == 'uz':
        text = "3️⃣ Shaharni tanlang:"
    else:
        text = "3️⃣ Выберите город:"
    
    await message.answer(
        text,
        reply_markup=get_cities_keyboard(cities, user.language)
    )
    await state.set_state(UstaXonaAddStates.choose_city)


@router.message(UstaXonaAddStates.enter_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    """Process phone number from text"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "❌ Bekor qilindi" if user.language == 'uz' else "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    phone = message.text.strip()
    if not phone.startswith('+'):
        phone = '+' + phone
    
    await state.update_data(phone=phone)
    user = await db.get_user(message.from_user.id)
    
    # Get cities for selection
    cities = await db.get_all_cities()
    
    if user.language == 'uz':
        text = "3️⃣ Shaharni tanlang:"
    else:
        text = "3️⃣ Выберите город:"
    
    await message.answer(
        text,
        reply_markup=get_cities_keyboard(cities, user.language)
    )
    await state.set_state(UstaXonaAddStates.choose_city)


@router.callback_query(UstaXonaAddStates.choose_city, F.data.startswith("city_"))
async def process_city(callback: CallbackQuery, state: FSMContext):
    """Process city selection"""
    city_id = int(callback.data.split("_")[1])
    logger.info(f"User {callback.from_user.id} selected city: {city_id}")
    await state.update_data(city_id=city_id)
    
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "4️⃣ Lokatsiyani yuboring yoki manzilni yozing:"
    else:
        text = "4️⃣ Отправьте локацию или напишите адрес:"
    
    await callback.message.answer(
        text,
        reply_markup=get_location_keyboard(user.language)
    )
    await state.set_state(UstaXonaAddStates.share_location)
    await callback.answer()


@router.message(UstaXonaAddStates.share_location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Process location sharing"""
    logger.info(f"User {message.from_user.id} shared location: {message.location.latitude}, {message.location.longitude}")
    await state.update_data(
        latitude=message.location.latitude,
        longitude=message.location.longitude
    )
    
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "5️⃣ Manzilni yozing (masalan: Chilonzor 12-kvartal):"
    else:
        text = "5️⃣ Напишите адрес (например: Чиланзар 12-квартал):"
    
    await message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.enter_address)


@router.message(UstaXonaAddStates.share_location, F.text)
async def process_address_directly(message: Message, state: FSMContext):
    """Process address from text without location"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "❌ Bekor qilindi" if user.language == 'uz' else "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(address=message.text)
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "6️⃣ Rasmni yuboring:"
    else:
        text = "6️⃣ Отправьте фото:"
    
    await message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.upload_photo)


@router.message(UstaXonaAddStates.enter_address)
async def process_address(message: Message, state: FSMContext):
    """Process address input"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "❌ Bekor qilindi" if user.language == 'uz' else "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(address=message.text)
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "6️⃣ Rasmni yuboring:"
    else:
        text = "6️⃣ Отправьте фото:"
    
    await message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.upload_photo)


@router.message(UstaXonaAddStates.upload_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Process photo upload"""
    logger.info(f"User {message.from_user.id} uploaded photo")
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)
    
    user = await db.get_user(message.from_user.id)
    brands = await db.get_all_car_brands()
    
    if user.language == 'uz':
        text = "7️⃣ Avtomobil markalarini tanlang:"
    else:
        text = "7️⃣ Выберите марки автомобилей:"
    
    await message.answer(
        text,
        reply_markup=get_car_brands_keyboard(user.language, brands)
    )
    await state.set_state(UstaXonaAddStates.choose_brands)


@router.message(UstaXonaAddStates.upload_photo, F.text)
async def skip_photo(message: Message, state: FSMContext):
    """Skip photo upload"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "❌ Bekor qilindi" if user.language == 'uz' else "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    user = await db.get_user(message.from_user.id)
    brands = await db.get_all_car_brands()
    
    if user.language == 'uz':
        text = "7️⃣ Avtomobil markalarini tanlang:"
    else:
        text = "7️⃣ Выберите марки автомобилей:"
    
    await message.answer(
        text,
        reply_markup=get_car_brands_keyboard(user.language, brands)
    )
    await state.set_state(UstaXonaAddStates.choose_brands)


@router.callback_query(UstaXonaAddStates.choose_brands, F.data.startswith("brand_"))
async def process_brand(callback: CallbackQuery, state: FSMContext):
    """Process brand selection"""
    brand_id = int(callback.data.split("_")[1])
    logger.info(f"User {callback.from_user.id} selected brand: {brand_id}")
    data = await state.get_data()
    
    # Store brand IDs
    brand_ids = data.get('brand_ids', [])
    if brand_id not in brand_ids:
        brand_ids.append(brand_id)
    
    await state.update_data(brand_ids=brand_ids)
    
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "8️⃣ Qisqacha ta'rif kiriting:"
    else:
        text = "8️⃣ Введите краткое описание:"
    
    await callback.message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(UstaXonaAddStates.enter_description)
    await callback.answer()


@router.message(UstaXonaAddStates.enter_description)
async def process_description(message: Message, state: FSMContext):
    """Process description and save usta xona"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        text = "❌ Bekor qilindi" if user.language == 'uz' else "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    description = None if message.text.lower() in ['keyingi', 'далее', 'skip'] else message.text
    
    # Get all data
    data = await state.get_data()
    user = await db.get_user(message.from_user.id)
    
    logger.info(f"User {message.from_user.id} submitting usta xona:")
    logger.info(f"  - Name: {data.get('service_name')}")
    logger.info(f"  - City ID: {data.get('city_id')}")
    logger.info(f"  - Phone: {data.get('phone')}")
    logger.info(f"  - Address: {data.get('address')}")
    logger.info(f"  - Brands: {data.get('brand_ids', [])}")
    logger.info(f"  - Has photo: {bool(data.get('photo_file_id'))}")
    logger.info(f"  - Has location: {bool(data.get('latitude'))}")
    
    # Create usta xona in database
    try:
        usta_xona = await db.create_usta_xona(
            owner_id=message.from_user.id,
            name=data['service_name'],
            city_id=data['city_id'],
            phone=data['phone'],
            address=data.get('address'),
            description=description,
            car_brand_ids=data.get('brand_ids', []),
            photo_file_id=data.get('photo_file_id'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        logger.info(f"Usta xona created successfully for user {message.from_user.id}, ID: {usta_xona.id}")
        
        if user.language == 'uz':
            text = "✅ Usta xona muvaffaqiyatli qo'shildi!\n\nAdmin tasdiqlashini kuting."
        else:
            text = "✅ Сервис успешно добавлен!\n\nОжидайте подтверждения администратора."
        
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        
        menu_text = "Asosiy menyu:" if user.language == 'uz' else "Главное меню:"
        await message.answer(menu_text, reply_markup=get_main_menu_keyboard(user.language))
        
    except Exception as e:
        logger.error(f"Error creating usta xona for user {message.from_user.id}: {str(e)}", exc_info=True)
        if user.language == 'uz':
            text = f"❌ Xatolik yuz berdi: {str(e)}"
        else:
            text = f"❌ Произошла ошибка: {str(e)}"
        
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
    
    await state.clear()

