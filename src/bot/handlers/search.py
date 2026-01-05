"""
Shop search handlers
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import (
    get_search_type_keyboard,
    get_car_brands_keyboard,
    get_cities_keyboard,
    Texts
)
from bot.utils import database as db
from bot.states import ShopSearchStates

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "usta_xona_search")
async def usta_xona_search_start(callback: CallbackQuery, state: FSMContext):
    """Start usta xona search"""
    logger.info(f"User {callback.from_user.id} started usta xona search")
    user = await db.get_user(callback.from_user.id)
    brands = await db.get_all_car_brands()
    
    # Filter out "Barchasi" / "Vse" from search brands
    brands = [b for b in brands if b.name_uz != 'Barchasi' and b.name_ru != 'Vse']
    
    if user.language == 'uz':
        text = "🔧 Usta xona qidirish\n\nAvtomobil markasini tanlang:"
    else:
        text = "🔧 Поиск сервиса\n\nВыберите марку автомобиля:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_car_brands_keyboard(user.language, brands)
    )
    await state.set_state(ShopSearchStates.choose_brand)
    await state.update_data(search_type="usta_xona")
    await callback.answer()


@router.callback_query(F.data == "shop_search")
async def shop_search_start(callback: CallbackQuery, state: FSMContext):
    """Start shop search"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "Qidirish turini tanlang:"
    else:
        text = "Выберите тип поиска:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_search_type_keyboard(user.language)
    )
    await callback.answer()


@router.callback_query(F.data == "search_by_model")
async def search_by_model(callback: CallbackQuery, state: FSMContext):
    """Search by car model"""
    user = await db.get_user(callback.from_user.id)
    brands = await db.get_all_car_brands()
    
    # Filter out "Barchasi" / "Vse" from search brands
    brands = [b for b in brands if b.name_uz != 'Barchasi' and b.name_ru != 'Все']
    
    if user.language == 'uz':
        text = "Avtomobil markasini tanlang:"
    else:
        text = "Выберите марку автомобиля:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_car_brands_keyboard(user.language, brands)
    )
    await state.set_state(ShopSearchStates.choose_brand)
    await callback.answer()


@router.callback_query(ShopSearchStates.choose_brand, F.data.startswith("brand_"))
async def process_brand_selection(callback: CallbackQuery, state: FSMContext):
    """Process brand selection and ask for city"""
    brand_id = int(callback.data.split("_")[1])
    brand = await db.get_car_brand(brand_id)
    
    if not brand:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
        return
    
    user = await db.get_user(callback.from_user.id)
    brand_name = brand.name_uz if user.language == 'uz' else brand.name_ru
    
    # Save selected brand
    await state.update_data(selected_brand=brand.id, brand_name=brand_name)
    
    user = await db.get_user(callback.from_user.id)
    cities = await db.get_all_cities()
    
    if user.language == 'uz':
        text = Texts.CHOOSE_CITY_UZ
    else:
        text = Texts.CHOOSE_CITY_RU
    
    await callback.message.edit_text(
        text,
        reply_markup=get_cities_keyboard(cities, user.language)
    )
    await state.set_state(ShopSearchStates.choose_city)
    await callback.answer()


@router.callback_query(ShopSearchStates.choose_city, F.data.startswith("city_"))
async def process_city_selection(callback: CallbackQuery, state: FSMContext):
    """Process city selection and show shops or usta xonalar"""
    city_id = int(callback.data.split("_")[1])
    city = await db.get_city(city_id)
    
    if not city:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
        return
    
    data = await state.get_data()
    brand_id = data.get('selected_brand')
    brand_name = data.get('brand_name', '')
    search_type = data.get('search_type', 'shop')
    
    user = await db.get_user(callback.from_user.id)
    
    # Check if searching for usta xona or shop
    if search_type == "usta_xona":
        logger.info(f"User {callback.from_user.id} searching usta xona: brand_id={brand_id}, city_id={city_id}")
        # Search usta xonalar
        usta_xonalar = await db.search_usta_xonalar(city_id, brand_id)
        
        logger.info(f"Found {len(usta_xonalar)} usta xonalar for user {callback.from_user.id}")
        
        if usta_xonalar:
            if user.language == 'uz':
                header_text = f"✅ {city.name_uz} shahrida {brand_name} uchun {len(usta_xonalar)} ta usta xona topildi:\n\n"
            else:
                header_text = f"✅ Найдено {len(usta_xonalar)} сервисов для {brand_name} в городе {city.name_ru}:\n\n"
            
            await callback.message.answer(header_text)
            
            # Send each usta xona
            for i, usta_xona in enumerate(usta_xonalar, 1):
                usta_text = f"{i}. 🔧 {usta_xona.name}\n"
                usta_text += f"📞 {usta_xona.phone}\n"
                if usta_xona.address:
                    usta_text += f"📍 {usta_xona.address}\n"
                if usta_xona.description:
                    usta_text += f"ℹ️ {usta_xona.description}\n"
                
                if usta_xona.photo_file_id:
                    try:
                        await callback.message.answer_photo(
                            photo=usta_xona.photo_file_id,
                            caption=usta_text
                        )
                    except Exception:
                        await callback.message.answer(usta_text)
                else:
                    await callback.message.answer(usta_text)
                
                if usta_xona.latitude and usta_xona.longitude:
                    try:
                        await callback.message.answer_location(
                            latitude=usta_xona.latitude,
                            longitude=usta_xona.longitude
                        )
                    except Exception:
                        pass
            
            if user.language == 'uz':
                final_text = "⬆️ Yuqorida topilgan usta xonalar"
            else:
                final_text = "⬆️ Найденные сервисы выше"
            
            await callback.message.answer(final_text)
        else:
            logger.warning(f"No usta xonalar found for user {callback.from_user.id}: brand_id={brand_id}, city_id={city_id}")
            if user.language == 'uz':
                result_text = f"❌ {city.name_uz} shahrida {brand_name} uchun usta xonalar topilmadi."
            else:
                result_text = f"❌ Сервисы для {brand_name} в городе {city.name_ru} не найдены."
            
            await callback.message.answer(result_text)
        
        await state.clear()
        await callback.answer()
        return
    
    # Search shops by brand (default behavior)
    shops = await db.search_shops(city_id, brand_id)
    
    user = await db.get_user(callback.from_user.id)
    
    if shops:
        if user.language == 'uz':
            header_text = f"✅ {city.name_uz} shahrida {brand_name} uchun {len(shops)} ta do'kon topildi:\n\n"
        else:
            header_text = f"✅ Найдено {len(shops)} магазинов для {brand_name} в городе {city.name_ru}:\n\n"
        
        await callback.message.answer(header_text)
        
        # Send each shop with photo and location
        for i, shop in enumerate(shops, 1):
            shop_text = f"{i}. {shop.name}\n"
            shop_text += f"📞 {shop.phone}\n"
            if shop.address:
                shop_text += f"📍 {shop.address}\n"
            if shop.description:
                shop_text += f"ℹ️ {shop.description}\n"
            
            # Add part categories with hashtags
            if user.language == 'uz' and shop.part_categories_uz:
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
                part_cats_clean = [remove_emoji(cat).strip() for cat in shop.part_categories_uz]
                part_cats_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in part_cats_clean])
                shop_text += f"📦 {part_cats_formatted}\n"
            elif user.language == 'ru' and shop.part_categories_ru:
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
                part_cats_clean = [remove_emoji(cat).strip() for cat in shop.part_categories_ru]
                part_cats_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in part_cats_clean])
                shop_text += f"📦 {part_cats_formatted}\n"
            
            # Try to send photo if exists
            if shop.photo_file_id:
                try:
                    await callback.message.answer_photo(
                        photo=shop.photo_file_id,
                        caption=shop_text
                    )
                except Exception as e:
                    # If photo fails (invalid file_id), send text only
                    await callback.message.answer(shop_text)
            else:
                await callback.message.answer(shop_text)
            
            # Send location if exists
            if shop.latitude and shop.longitude:
                try:
                    await callback.message.answer_location(
                        latitude=shop.latitude,
                        longitude=shop.longitude
                    )
                except Exception:
                    pass  # Skip if location fails
        
        result_text = ""  # Already sent shops individually
    else:
        if user.language == 'uz':
            result_text = f"❌ {city.name_uz} shahrida {brand_name} uchun do'konlar topilmadi.\n\n"
            result_text += "So'rov qoldirishingiz mumkin."
        else:
            result_text = f"❌ Магазины для {brand_name} в городе {city.name_ru} не найдены.\n\n"
            result_text += "Вы можете оставить запрос."
    
    # Add buttons
    from bot.keyboards.inline import InlineKeyboardBuilder, InlineKeyboardButton
    keyboard = InlineKeyboardBuilder()
    
    # If no shops found, add "Leave request" button
    if not shops:
        if user.language == 'uz':
            keyboard.row(InlineKeyboardButton(text="📝 So'rov qoldirish", callback_data="leave_request"))
        else:
            keyboard.row(InlineKeyboardButton(text="📝 Оставить запрос", callback_data="leave_request"))
    
    if user.language == 'uz':
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_UZ, callback_data="back_to_search"))
    else:
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_RU, callback_data="back_to_search"))
    
    # Send result message if exists (no shops found case)
    if result_text:
        await callback.message.answer(
            result_text,
            reply_markup=keyboard.as_markup()
        )
    else:
        # Just send back button for shops found case
        if user.language == 'uz':
            back_text = "⬆️ Yuqorida topilgan do'konlar"
            keyboard.row(InlineKeyboardButton(text="🔧 Usta xonalar ham kerak bo'ladimi?", callback_data="ask_usta_xona"))
        else:
            back_text = "⬆️ Найденные магазины выше"
            keyboard.row(InlineKeyboardButton(text="🔧 Нужны ли также сервисы?", callback_data="ask_usta_xona"))
        
        await callback.message.answer(
            back_text,
            reply_markup=keyboard.as_markup()
        )
    
    # Save search params for potential usta xona search
    await state.update_data(
        last_search_city_id=city_id,
        last_search_brand_id=brand_id,
        last_search_city_name=city.name_uz if user.language == 'uz' else city.name_ru,
        last_search_brand_name=brand_name
    )
    
    await callback.answer()


@router.callback_query(F.data == "back_to_search")
async def back_to_search(callback: CallbackQuery, state: FSMContext):
    """Back to search type selection"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "Qidirish turini tanlang:"
    else:
        text = "Выберите тип поиска:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_search_type_keyboard(user.language)
    )
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "back_to_brands")
async def back_to_brands(callback: CallbackQuery, state: FSMContext):
    """Back to brand selection"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "Avtomobil markasini tanlang:"
    else:
        text = "Выберите марку автомобиля:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_car_brands_keyboard(user.language)
    )
    await state.set_state(ShopSearchStates.choose_brand)
    await callback.answer()


@router.callback_query(F.data == "ask_usta_xona")
async def ask_usta_xona(callback: CallbackQuery, state: FSMContext):
    """Ask if user needs usta xona too"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "🔧 Sizga usta xonalar ham kerakmi?\n\n"
        text += "Usta xonalar - avtomobil ta'mirlash xizmatlari:\n"
        text += "• 🔧 Ta'mirlash\n"
        text += "• 🛠 Texservis\n"  
        text += "• 🚗 Diagnostika"
    else:
        text = "🔧 Нужны ли вам также сервисы?\n\n"
        text += "Сервисы - услуги по ремонту автомобилей:\n"
        text += "• 🔧 Ремонт\n"
        text += "• 🛠 Техсервис\n"
        text += "• 🚗 Диагностика"
    
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    keyboard = InlineKeyboardBuilder()
    if user.language == 'uz':
        keyboard.row(InlineKeyboardButton(text="✅ Ha, kerak", callback_data="search_usta_xona_yes"))
        keyboard.row(InlineKeyboardButton(text="❌ Yo'q", callback_data="search_usta_xona_no"))
    else:
        keyboard.row(InlineKeyboardButton(text="✅ Да, нужны", callback_data="search_usta_xona_yes"))
        keyboard.row(InlineKeyboardButton(text="❌ Нет", callback_data="search_usta_xona_no"))
    
    await callback.message.answer(text, reply_markup=keyboard.as_markup())
    await callback.answer()


@router.callback_query(F.data == "search_usta_xona_yes")
async def search_usta_xona_yes(callback: CallbackQuery, state: FSMContext):
    """Show usta xonalar using same search parameters"""
    logger.info(f"User {callback.from_user.id} requested usta xona after shop search")
    user = await db.get_user(callback.from_user.id)
    data = await state.get_data()
    
    city_id = data.get('last_search_city_id')
    brand_id = data.get('last_search_brand_id')
    city_name = data.get('last_search_city_name', '')
    brand_name = data.get('last_search_brand_name', '')
    
    logger.info(f"Using saved search params: brand_id={brand_id}, city_id={city_id}")
    
    if not city_id or not brand_id:
        # Fallback: ask to search again
        brands = await db.get_all_car_brands()
        brands = [b for b in brands if b.name_uz != 'Barchasi' and b.name_ru != 'Vse']
        
        if user.language == 'uz':
            text = "🔧 Usta xonalar qidirish\n\nAvtomobil markasini tanlang:"
        else:
            text = "🔧 Поиск сервисов\n\nВыберите марку автомобиля:"
        
        await callback.message.answer(
            text,
            reply_markup=get_car_brands_keyboard(user.language, brands)
        )
        await state.set_state(ShopSearchStates.choose_brand)
        await state.update_data(search_type="usta_xona")
        await callback.answer()
        return
    
    # Search usta xonalar with same params
    logger.info(f"Searching usta xonalar with saved params for user {callback.from_user.id}")
    usta_xonalar = await db.search_usta_xonalar(city_id, brand_id)
    
    logger.info(f"Found {len(usta_xonalar)} usta xonalar from saved search")
    
    if usta_xonalar:
        if user.language == 'uz':
            header_text = f"✅ {city_name} shahrida {brand_name} uchun {len(usta_xonalar)} ta usta xona topildi:\n\n"
        else:
            header_text = f"✅ Найдено {len(usta_xonalar)} сервисов для {brand_name} в городе {city_name}:\n\n"
        
        await callback.message.answer(header_text)
        
        # Send each usta xona with photo and location
        for i, usta_xona in enumerate(usta_xonalar, 1):
            usta_text = f"{i}. 🔧 {usta_xona.name}\n"
            usta_text += f"📞 {usta_xona.phone}\n"
            if usta_xona.address:
                usta_text += f"📍 {usta_xona.address}\n"
            if usta_xona.description:
                usta_text += f"ℹ️ {usta_xona.description}\n"
            
            # Add service types with hashtags if available
            if user.language == 'uz' and usta_xona.service_types_uz:
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
                service_types_clean = [remove_emoji(cat).strip() for cat in usta_xona.service_types_uz]
                service_types_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in service_types_clean])
                usta_text += f"🛠 {service_types_formatted}\n"
            elif user.language == 'ru' and usta_xona.service_types_ru:
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
                service_types_clean = [remove_emoji(cat).strip() for cat in usta_xona.service_types_ru]
                service_types_formatted = ' '.join([f'#{cat.replace(" ", "")}' for cat in service_types_clean])
                usta_text += f"🛠 {service_types_formatted}\n"
            
            # Try to send photo if exists
            if usta_xona.photo_file_id:
                try:
                    await callback.message.answer_photo(
                        photo=usta_xona.photo_file_id,
                        caption=usta_text
                    )
                except Exception:
                    # If photo fails, send text only
                    await callback.message.answer(usta_text)
            else:
                await callback.message.answer(usta_text)
            
            # Send location if exists
            if usta_xona.latitude and usta_xona.longitude:
                try:
                    await callback.message.answer_location(
                        latitude=usta_xona.latitude,
                        longitude=usta_xona.longitude
                    )
                except Exception:
                    pass
        
        if user.language == 'uz':
            final_text = "⬆️ Yuqorida topilgan usta xonalar"
        else:
            final_text = "⬆️ Найденные сервисы выше"
        
        await callback.message.answer(final_text)
    else:
        if user.language == 'uz':
            result_text = f"❌ {city_name} shahrida {brand_name} uchun usta xonalar topilmadi."
        else:
            result_text = f"❌ Сервисы для {brand_name} в городе {city_name} не найдены."
        
        await callback.message.answer(result_text)
    
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "search_usta_xona_no")
async def search_usta_xona_no(callback: CallbackQuery, state: FSMContext):
    """User doesn't need usta xona"""
    user = await db.get_user(callback.from_user.id)
    
    if user.language == 'uz':
        text = "👍 Tushunarli. Agar kerak bo'lsa, qayta qidirishingiz mumkin."
    else:
        text = "👍 Понятно. Если потребуется, можете найти через поиск."
    
    await callback.message.answer(text)
    await callback.answer()
