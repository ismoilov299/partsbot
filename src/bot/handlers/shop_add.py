"""
Shop add handlers - full implementation
"""
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_cities_keyboard, get_car_brands_keyboard, Texts, get_cancel_keyboard, get_phone_keyboard, get_location_keyboard, get_part_categories_keyboard
from bot.utils import db
from bot.states import ShopAddStates

router = Router()


@router.callback_query(F.data == "shop_add")
async def shop_add_start(callback: CallbackQuery, state: FSMContext):
    """Start shop addition process - ask for shop name"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "✅ Do'kon qo'shish\n\n1️⃣ Do'kon nomini kiriting:"
    else:
        text = "✅ Добавление магазина\n\n1️⃣ Введите название магазина:"
    
    await callback.message.answer(
        text,
        reply_markup=get_cancel_keyboard(user.language)
    )
    await state.set_state(ShopAddStates.enter_shop_name)
    await callback.answer()


@router.message(ShopAddStates.enter_shop_name)
async def process_shop_name(message: Message, state: FSMContext):
    """Process shop name and ask for phone"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(shop_name=message.text)
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "2️⃣ Telefon raqamingizni kiriting yoki tugmani bosing:\n\n"
        text += "Masalan: +998901234567\n"
        text += "Yoki 📱 tugmasini bosing"
    else:
        text = "2️⃣ Введите номер телефона или нажмите кнопку:\n\n"
        text += "Например: +998901234567\n"
        text += "Или нажмите кнопку 📱"
    
    await message.answer(text, reply_markup=get_phone_keyboard(user.language))
    await state.set_state(ShopAddStates.enter_phone)


@router.message(ShopAddStates.enter_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone via contact button"""
    phone = message.contact.phone_number
    
    # Format phone number
    if not phone.startswith('+'):
        phone = '+' + phone
    
    await state.update_data(phone=phone)
    user = await db.get_user(message.from_user.id)
    cities = await db.get_all_cities()
    
    if user.language == 'uz':
        text = "✅ Raqam qabul qilindi!\n\n3️⃣ Do'koningiz qaysi shaharda joylashgan?"
    else:
        text = "✅ Номер принят!\n\n3️⃣ В каком городе находится ваш магазин?"
    
    await message.answer(
        text,
        reply_markup=get_cities_keyboard(cities, user.language)
    )
    await state.set_state(ShopAddStates.choose_city)


@router.message(ShopAddStates.enter_phone, F.text)
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
    
    # Validate phone number (simple check)
    phone = message.text.strip()
    
    # Check if contains only digits, +, -, (, ), spaces
    import re
    if not re.match(r'^[\d\+\-\(\)\s]+$', phone):
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Noto'g'ri format!\n\nIltimos, telefon raqamini to'g'ri kiriting:\nMasalan: +998901234567"
        else:
            text = "❌ Неверный формат!\n\nПожалуйста, введите номер телефона правильно:\nНапример: +998901234567"
        await message.answer(text)
        return
    
    # Ensure phone starts with +
    if not phone.startswith('+'):
        phone = '+' + phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    await state.update_data(phone=phone)
    user = await db.get_user(message.from_user.id)
    cities = await db.get_all_cities()
    
    if user.language == 'uz':
        text = "✅ Raqam qabul qilindi!\n\n3️⃣ Do'koningiz qaysi shaharda joylashgan?"
    else:
        text = "✅ Номер принят!\n\n3️⃣ В каком городе находится ваш магазин?"
    
    await message.answer(
        text,
        reply_markup=get_cities_keyboard(cities, user.language)
    )
    await state.set_state(ShopAddStates.choose_city)


@router.callback_query(ShopAddStates.choose_city, F.data.startswith("city_"))
async def process_city(callback: CallbackQuery, state: FSMContext):
    """Process city selection and ask for location"""
    city_id = int(callback.data.split("_")[1])
    city = await db.get_city(city_id)
    
    if not city:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
        return
    
    await state.update_data(city_id=city_id)
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = f"4️⃣ Do'kon lokatsiyasini yuboring:\n\n"
        text += "📍 'Lokatsiya yuborish' tugmasini bosing yoki o'tkazib yuboring"
    else:
        text = f"4️⃣ Отправьте локацию магазина:\n\n"
        text += "📍 Нажмите кнопку 'Отправить локацию' или пропустите"
    
    await callback.message.answer(text, reply_markup=get_location_keyboard(user.language))
    await state.set_state(ShopAddStates.share_location)
    await callback.answer()


@router.message(ShopAddStates.share_location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Process location and ask for address"""
    latitude = message.location.latitude
    longitude = message.location.longitude
    
    await state.update_data(
        latitude=latitude,
        longitude=longitude
    )
    
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = f"✅ Lokatsiya qabul qilindi!\n\n5️⃣ Endi aniq manzilni kiriting:\n\nMasalan: Chilonzor, 12-kvartal, 5-uy"
    else:
        text = f"✅ Локация получена!\n\n5️⃣ Теперь введите точный адрес:\n\nНапример: Чиланзар, 12-квартал, дом 5"
    
    await message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(ShopAddStates.enter_address)


@router.message(ShopAddStates.share_location)
async def process_skip_location(message: Message, state: FSMContext):
    """Handle skip location or cancel"""
    user = await db.get_user(message.from_user.id)
    
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    # Check if user wants to skip
    skip_keywords_uz = ["o'tkazib", "otkazib", "skip"]
    skip_keywords_ru = ["пропустить", "пропуск"]
    
    is_skip = any(keyword in message.text.lower() for keyword in skip_keywords_uz + skip_keywords_ru)
    
    if is_skip or message.text == "⏩ O'tkazib yuborish" or message.text == "⏩ Пропустить":
        # Skip location
        await state.update_data(latitude=None, longitude=None)
        
        if user.language == 'uz':
            text = "5️⃣ Do'kon manzilini kiriting:\n\nMasalan: Chilonzor, 12-kvartal, 5-uy"
        else:
            text = "5️⃣ Введите адрес магазина:\n\nНапример: Чиланзар, 12-квартал, дом 5"
        
        await message.answer(text, reply_markup=get_cancel_keyboard(user.language))
        await state.set_state(ShopAddStates.enter_address)
    else:
        # Ask to send location again
        if user.language == 'uz':
            text = "❌ Iltimos, lokatsiya yuboring yoki 'O'tkazib yuborish' tugmasini bosing"
        else:
            text = "❌ Пожалуйста, отправьте локацию или нажмите 'Пропустить'"
        await message.answer(text)


@router.message(ShopAddStates.enter_address)
async def process_address(message: Message, state: FSMContext):
    """Process address and ask for photo"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(address=message.text)
    user = await db.get_user(message.from_user.id)
    
    if user.language == 'uz':
        text = "6️⃣ Do'kon old tomonining rasmini yuboring:\n\n📸 Faqat bitta rasm yuboring"
    else:
        text = "6️⃣ Отправьте фото фасада магазина:\n\n📸 Отправьте только одно фото"
    
    await message.answer(text, reply_markup=get_cancel_keyboard(user.language))
    await state.set_state(ShopAddStates.upload_photo)


@router.message(ShopAddStates.upload_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Process photo and ask for car brands"""
    # Save photo file_id
    photo = message.photo[-1]  # Get largest photo
    await state.update_data(photo_file_id=photo.file_id)
    
    user = await db.get_user(message.from_user.id)
    brands = await db.get_all_car_brands()
    
    if user.language == 'uz':
        text = "7️⃣ Qaysi avtomobil markalari uchun ehtiyot qismlar sotasiz?\n\nKeraklisini tanlang (bir yoki bir nechtasini):"
    else:
        text = "7️⃣ Для каких марок автомобилей продаете запчасти?\n\nВыберите нужные (один или несколько):"
    
    await message.answer(
        text,
        reply_markup=get_car_brands_keyboard(user.language, brands)
    )
    await state.set_state(ShopAddStates.choose_brands)


@router.message(ShopAddStates.upload_photo)
async def process_photo_error(message: Message, state: FSMContext):
    """Handle non-photo messages"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    user = await db.get_user(message.from_user.id)
    if user.language == 'uz':
        text = "❌ Iltimos, rasm yuboring!"
    else:
        text = "❌ Пожалуйста, отправьте фото!"
    
    await message.answer(text)


@router.callback_query(ShopAddStates.choose_brands, F.data.startswith("brand_"))
async def process_brands(callback: CallbackQuery, state: FSMContext):
    """Process brand selection and ask for description"""
    brand_id = int(callback.data.split("_")[1])
    brand = await db.get_car_brand(brand_id)
    
    if not brand:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
        return
    
    user = await db.get_user(callback.from_user.id)
    
    # If "Barchasi" / "Vse" selected, add all brands except "Barchasi" itself
    if brand.name_uz == 'Barchasi' or brand.name_ru == 'Все':
        all_brands = await db.get_all_car_brands()
        # Filter out "Barchasi" itself
        all_brands = [b for b in all_brands if b.name_uz != 'Barchasi' and b.name_ru != 'Все']
        brand_ids = [b.id for b in all_brands]
        if user.language == 'uz':
            brand_names = [b.name_uz for b in all_brands]
        else:
            brand_names = [b.name_ru for b in all_brands]
        await state.update_data(brand_ids=brand_ids, brand_names=brand_names)
    else:
        brand_name = brand.name_uz if user.language == 'uz' else brand.name_ru
        await state.update_data(brand_ids=[brand.id], brand_names=[brand_name])
    
    if user.language == 'uz':
        text = f"8️⃣ Qanday turdagi ehtiyot qismlar sotasiz?\n\nKerakli toifalarni tanlang (bir yoki bir nechtasini):"
    else:
        text = f"8️⃣ Какие категории запчастей продаете?\n\nВыберите нужные категории (одну или несколько):"
    
    await callback.message.answer(text, reply_markup=get_part_categories_keyboard(user.language))
    await state.update_data(selected_categories=[])
    await state.set_state(ShopAddStates.choose_part_categories)
    await callback.answer()


@router.callback_query(ShopAddStates.choose_part_categories, F.data.startswith("partcat_"))
async def process_part_category(callback: CallbackQuery, state: FSMContext):
    """Process part category selection"""
    data = await state.get_data()
    selected = data.get('selected_categories', [])
    user = await db.get_user(callback.from_user.id)
    
    if callback.data == "partcat_done":
        # User finished selecting
        if not selected:
            await callback.answer("Kamida bitta toifa tanlang!", show_alert=True)
            return
        
        # Get category names
        category_names_uz = [Texts.PART_CATEGORIES[i]['uz'] for i in selected]
        category_names_ru = [Texts.PART_CATEGORIES[i]['ru'] for i in selected]
        
        await state.update_data(
            part_categories_uz=category_names_uz,
            part_categories_ru=category_names_ru,
            description=""  # Set empty description
        )
        
        # Skip description and go directly to confirmation
        await callback.answer()
        
        # Show confirmation directly
        data = await state.get_data()
        
        # Get city name
        city = await db.get_city(data['city_id'])
        city_name = city.name_uz if user.language == 'uz' else city.name_ru
        
        # Get part categories - remove emojis from hashtags
        import re
        def remove_emoji(text):
            # Remove emojis and keep only text
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
        
        part_categories_uz_clean = [remove_emoji(cat).strip() for cat in category_names_uz]
        part_categories_ru_clean = [remove_emoji(cat).strip() for cat in category_names_ru]
        part_categories_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in part_categories_uz_clean]) if user.language == 'uz' else ' '.join([f'#{cat.replace(" ", "")}' for cat in part_categories_ru_clean])
        
        # Create confirmation message
        if user.language == 'uz':
            confirm_text = "✅ Ma'lumotlarni tasdiqlang:\n\n"
            confirm_text += f"📝 Do'kon nomi: {data['shop_name']}\n"
            confirm_text += f"📞 Telefon: {data['phone']}\n"
            confirm_text += f"🏙 Shahar: {city_name}\n"
            confirm_text += f"📍 Manzil: {data['address']}\n"
            confirm_text += f"🚗 Markalar: {', '.join(data['brand_names'])}\n"
            if part_categories_formatted:
                confirm_text += f"📦 Toifalar: {part_categories_formatted}\n"
            confirm_text += "\nMa'lumotlar to'g'rimi?"
        else:
            confirm_text = "✅ Подтвердите данные:\n\n"
            confirm_text += f"📝 Название: {data['shop_name']}\n"
            confirm_text += f"📞 Телефон: {data['phone']}\n"
            confirm_text += f"🏙 Город: {city_name}\n"
            confirm_text += f"📍 Адрес: {data['address']}\n"
            confirm_text += f"🚗 Марки: {', '.join(data['brand_names'])}\n"
            if part_categories_formatted:
                confirm_text += f"📦 Категории: {part_categories_formatted}\n"
            confirm_text += "\nДанные верны?"
        
        # Send photo with confirmation
        from aiogram.types import InlineKeyboardButton
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        
        keyboard = InlineKeyboardBuilder()
        if user.language == 'uz':
            keyboard.row(InlineKeyboardButton(text="✅ Ha, to'g'ri", callback_data="confirm_shop_yes"))
            keyboard.row(InlineKeyboardButton(text="❌ Yo'q, qayta", callback_data="confirm_shop_no"))
        else:
            keyboard.row(InlineKeyboardButton(text="✅ Да, верно", callback_data="confirm_shop_yes"))
            keyboard.row(InlineKeyboardButton(text="❌ Нет, заново", callback_data="confirm_shop_no"))
        
        await callback.message.answer_photo(
            photo=data['photo_file_id'],
            caption=confirm_text,
            reply_markup=keyboard.as_markup()
        )
        await state.set_state(ShopAddStates.confirm)
    else:
        # Toggle category selection
        cat_id = int(callback.data.split("_")[1])
        
        if cat_id in selected:
            selected.remove(cat_id)
        else:
            selected.append(cat_id)
        
        await state.update_data(selected_categories=selected)
        
        # Update keyboard
        await callback.message.edit_reply_markup(
            reply_markup=get_part_categories_keyboard(user.language, selected)
        )
        await callback.answer()


@router.message(ShopAddStates.enter_description)
async def process_description(message: Message, state: FSMContext):
    """Process description and show confirmation"""
    if message.text in [Texts.CANCEL_UZ, Texts.CANCEL_RU]:
        await state.clear()
        user = await db.get_user(message.from_user.id)
        if user.language == 'uz':
            text = "❌ Bekor qilindi"
        else:
            text = "❌ Отменено"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        return
    
    await state.update_data(description=message.text)
    data = await state.get_data()
    user = await db.get_user(message.from_user.id)
    
    # Get city name
    city = await db.get_city(data['city_id'])
    city_name = city.name_uz if user.language == 'uz' else city.name_ru
    
    # Get part categories - remove emojis from hashtags
    import re
    def remove_emoji(text):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    
    part_categories = data.get('part_categories_uz') if user.language == 'uz' else data.get('part_categories_ru')
    part_categories_clean = [remove_emoji(cat).strip() for cat in part_categories] if part_categories else []
    part_categories_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in part_categories_clean]) if part_categories_clean else ''
    
    # Create confirmation message
    if user.language == 'uz':
        confirm_text = "✅ Ma'lumotlarni tasdiqlang:\n\n"
        confirm_text += f"📝 Do'kon nomi: {data['shop_name']}\n"
        confirm_text += f"📞 Telefon: {data['phone']}\n"
        confirm_text += f"🏙 Shahar: {city_name}\n"
        confirm_text += f"📍 Manzil: {data['address']}\n"
        confirm_text += f"🚗 Markalar: {', '.join(data['brand_names'])}\n"
        if part_categories_formatted:
            confirm_text += f"📦 Toifalar: {part_categories_formatted}\n"
        confirm_text += f"ℹ️ Tavsif: {data['description']}\n\n"
        confirm_text += "Ma'lumotlar to'g'rimi?"
    else:
        confirm_text = "✅ Подтвердите данные:\n\n"
        confirm_text += f"📝 Название: {data['shop_name']}\n"
        confirm_text += f"📞 Телефон: {data['phone']}\n"
        confirm_text += f"🏙 Город: {city_name}\n"
        confirm_text += f"📍 Адрес: {data['address']}\n"
        confirm_text += f"🚗 Марки: {', '.join(data['brand_names'])}\n"
        if part_categories_formatted:
            confirm_text += f"📦 Категории: {part_categories_formatted}\n"
        confirm_text += f"ℹ️ Описание: {data['description']}\n\n"
        confirm_text += "Данные верны?"
    
    # Send photo with confirmation
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    keyboard = InlineKeyboardBuilder()
    if user.language == 'uz':
        keyboard.row(InlineKeyboardButton(text="✅ Ha, to'g'ri", callback_data="confirm_shop_yes"))
        keyboard.row(InlineKeyboardButton(text="❌ Yo'q, qayta", callback_data="confirm_shop_no"))
    else:
        keyboard.row(InlineKeyboardButton(text="✅ Да, верно", callback_data="confirm_shop_yes"))
        keyboard.row(InlineKeyboardButton(text="❌ Нет, заново", callback_data="confirm_shop_no"))
    
    await message.answer_photo(
        photo=data['photo_file_id'],
        caption=confirm_text,
        reply_markup=keyboard.as_markup()
    )
    await message.answer("👆", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ShopAddStates.confirm)


@router.callback_query(ShopAddStates.confirm, F.data == "confirm_shop_yes")
async def confirm_shop(callback: CallbackQuery, state: FSMContext):
    """Save shop to database"""
    data = await state.get_data()
    user = await db.get_user(callback.from_user.id)
    
    try:
        # Save shop to database (not approved yet)
        shop = await db.create_shop(
            owner_id=callback.from_user.id,
            name=data['shop_name'],
            city_id=data['city_id'],
            phone=data['phone'],
            address=data['address'],
            description=data['description'],
            car_brand_ids=data['brand_ids'],
            photo_file_id=data['photo_file_id'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            part_categories_uz=data.get('part_categories_uz'),
            part_categories_ru=data.get('part_categories_ru')
        )
        
        # Send to user
        if user.language == 'uz':
            text = "✅ Ma'lumotlar qabul qilindi!\n\n"
            text += "Do'koningiz admin tomonidan ko'rib chiqilmoqda.\n"
            text += "Tasdiqlangandan so'ng foydalanuvchilar do'koningizni topishi mumkin bo'ladi.\n\n"
            text += "Tez orada sizga xabar beramiz!"
        else:
            text = "✅ Данные приняты!\n\n"
            text += "Ваш магазин проверяется администратором.\n"
            text += "После одобрения пользователи смогут найти ваш магазин.\n\n"
            text += "Скоро сообщим!"
        
        await callback.message.answer(text)
        
        # Send to admin for approval
        admin_chat_id = os.getenv('ADMIN_CHAT_ID')
        if admin_chat_id:
            try:
                # Get city name
                city = await db.get_city(data['city_id'])
                city_name = f"{city.name_uz} / {city.name_ru}"
                
                # Create admin message
                admin_text = "🏪 YANGI DO'KON - TEKSHIRISH KERAK\n\n"
                admin_text += f"👤 Egasi: {user.first_name}"
                if user.username:
                    admin_text += f" (@{user.username})"
                admin_text += f"\n📱 ID: {user.telegram_id}"
                admin_text += f"\n\n📝 Nomi: {data['shop_name']}"
                admin_text += f"\n📞 Telefon: {data['phone']}"
                admin_text += f"\n🏙 Shahar: {city_name}"
                admin_text += f"\n📍 Manzil: {data['address']}"
                
                # Add location info if exists
                if data.get('latitude') and data.get('longitude'):
                    admin_text += f"\n🌐 Koordinatalar: {data['latitude']}, {data['longitude']}"
                
                admin_text += f"\n🚗 Brendlar: {', '.join(data['brand_names'])}\n"
                
                # Add part categories with hashtags - remove emojis
                part_cats_ru = data.get('part_categories_ru')
                if part_cats_ru:
                    import re
                    def remove_emoji(text):
                        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F300-\U0001F5FF"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
                        return emoji_pattern.sub(r'', text)
                    part_cats_clean = [remove_emoji(cat).strip() for cat in part_cats_ru]
                    part_cats_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in part_cats_clean])
                    admin_text += f"📦 Qismlar: {part_cats_formatted}\n"
                
                admin_text += f"\n🆔 Do'kon ID: {shop.id}"
                
                # Create approval buttons
                from aiogram.types import InlineKeyboardButton
                from aiogram.utils.keyboard import InlineKeyboardBuilder
                
                admin_keyboard = InlineKeyboardBuilder()
                admin_keyboard.row(
                    InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_shop_{shop.id}"),
                    InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_shop_{shop.id}")
                )
                
                # Send to admin with photo
                from aiogram import Bot
                bot = Bot(token=os.getenv('BOT_TOKEN'))
                await bot.send_photo(
                    chat_id=admin_chat_id,
                    photo=data['photo_file_id'],
                    caption=admin_text,
                    reply_markup=admin_keyboard.as_markup()
                )
                
                # Send location if exists
                if data.get('latitude') and data.get('longitude'):
                    await bot.send_location(
                        chat_id=admin_chat_id,
                        latitude=data['latitude'],
                        longitude=data['longitude']
                    )
                
            except Exception as e:
                print(f"Error sending to admin: {e}")
        
        # Send main menu before clearing state
        from ..keyboards.inline import get_main_menu_keyboard
        if user.language == 'uz':
            menu_text = "Asosiy menyu:"
        else:
            menu_text = "Главное меню:"
        await callback.message.answer(menu_text, reply_markup=get_main_menu_keyboard(user.language))
        
        await state.clear()
        
    except Exception as e:
        if user.language == 'uz':
            text = f"❌ Xatolik yuz berdi: {str(e)}\n\nIltimos, qayta urinib ko'ring."
        else:
            text = f"❌ Произошла ошибка: {str(e)}\n\nПожалуйста, попробуйте снова."
        
        await callback.message.answer(text)
        await state.clear()
    
    await callback.answer()


@router.callback_query(ShopAddStates.confirm, F.data == "confirm_shop_no")
async def cancel_shop(callback: CallbackQuery, state: FSMContext):
    """Cancel shop addition"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "❌ Bekor qilindi.\n\nQaytadan boshlash uchun 'Do'kon kiritish' tugmasini bosing."
    else:
        text = "❌ Отменено.\n\nЧтобы начать заново, нажмите кнопку 'Добавить магазин'."
    
    await callback.message.answer(text)
    await state.clear()
    await callback.answer()
