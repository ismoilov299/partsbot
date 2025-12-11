"""
Shop search handlers
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import (
    get_search_type_keyboard,
    get_car_brands_keyboard,
    get_cities_keyboard,
    Texts
)
from bot.utils import db
from bot.states import ShopSearchStates

router = Router()


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
    """Process city selection and show shops"""
    city_id = int(callback.data.split("_")[1])
    city = await db.get_city(city_id)
    
    if not city:
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
        return
    
    data = await state.get_data()
    brand_id = data.get('selected_brand')
    brand_name = data.get('brand_name', '')
    
    # Search shops by brand
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
            
            # Send photo if exists
            if shop.photo_file_id:
                await callback.message.answer_photo(
                    photo=shop.photo_file_id,
                    caption=shop_text
                )
            else:
                await callback.message.answer(shop_text)
            
            # Send location if exists
            if shop.latitude and shop.longitude:
                await callback.message.answer_location(
                    latitude=shop.latitude,
                    longitude=shop.longitude
                )
        
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
        else:
            back_text = "⬆️ Найденные магазины выше"
        
        await callback.message.answer(
            back_text,
            reply_markup=keyboard.as_markup()
        )
    
    await state.clear()
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
