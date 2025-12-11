"""
Keyboards for the bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Texts:
    """Text constants for different languages"""
    
    # Language selection
    CHOOSE_LANGUAGE_UZ = "Tilni tanlang"
    CHOOSE_LANGUAGE_RU = "Выберите язык"
    
    # Main menu
    MAIN_MENU_UZ = "Asosiy menyu"
    MAIN_MENU_RU = "Главное меню"
    SHOP_SEARCH_UZ = "🔍 Do'kon qidirish"
    SHOP_SEARCH_RU = "🔍 Поиск магазина"
    SHOP_ADD_UZ = "➕ Do'kon kiritish"
    SHOP_ADD_RU = "➕ Добавить магазин"
    
    # Shop search
    SEARCH_BY_MODEL_UZ = "🚗 Model bo'yicha qidirish"
    SEARCH_BY_MODEL_RU = "🚗 Поиск по модели"
    LEAVE_REQUEST_UZ = "📝 So'rov qoldirish"
    LEAVE_REQUEST_RU = "📝 Оставить запрос"
    
    # City selection
    CHOOSE_CITY_UZ = "Qaysi shahardagi do'konlar kerak?"
    CHOOSE_CITY_RU = "Магазины в каком городе нужны?"
    
    # Car brands
    CAR_BRANDS = [
        "KIA/HYUNDAI",
        "CHEVROLET GM",
        "CHERY/JETOUR/HAVAL",
        "BYD",
        "BMW",
        "MERCEDES BENZ",
        "Другие Иномарки"
    ]
    
    BACK_UZ = "⬅️ Ortga"
    BACK_RU = "⬅️ Назад"
    CANCEL_UZ = "❌ Bekor qilish"
    CANCEL_RU = "❌ Отменить"
    
    # Part categories
    PART_CATEGORIES = [
        {"uz": "🔧 Motor va hodovoy", "ru": "🔧 Двигатель и ходовая"},
        {"uz": "🚗 Kuzov qismlari", "ru": "🚗 Кузовные детали"},
        {"uz": "✨ Tuning", "ru": "✨ Тюнинг"},
        {"uz": "🛢 Yog'lar va antifrizlar", "ru": "🛢 Масла и антифризы"},
        {"uz": "⚡️ Elektronika", "ru": "⚡️ Электроника"},
        {"uz": "📦 Boshqalar", "ru": "📦 Другие"},
    ]


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
    )
    return keyboard.as_markup()


def get_main_menu_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = InlineKeyboardBuilder()
    
    if language == 'uz':
        keyboard.row(InlineKeyboardButton(text=Texts.SHOP_SEARCH_UZ, callback_data="shop_search"))
        keyboard.row(InlineKeyboardButton(text=Texts.SHOP_ADD_UZ, callback_data="shop_add"))
    else:
        keyboard.row(InlineKeyboardButton(text=Texts.SHOP_SEARCH_RU, callback_data="shop_search"))
        keyboard.row(InlineKeyboardButton(text=Texts.SHOP_ADD_RU, callback_data="shop_add"))
    
    return keyboard.as_markup()


def get_search_type_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Get search type selection keyboard"""
    keyboard = InlineKeyboardBuilder()
    
    if language == 'uz':
        keyboard.row(InlineKeyboardButton(text=Texts.SEARCH_BY_MODEL_UZ, callback_data="search_by_model"))
        keyboard.row(InlineKeyboardButton(text=Texts.LEAVE_REQUEST_UZ, callback_data="leave_request"))
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_UZ, callback_data="back_to_main"))
    else:
        keyboard.row(InlineKeyboardButton(text=Texts.SEARCH_BY_MODEL_RU, callback_data="search_by_model"))
        keyboard.row(InlineKeyboardButton(text=Texts.LEAVE_REQUEST_RU, callback_data="leave_request"))
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_RU, callback_data="back_to_main"))
    
    return keyboard.as_markup()


def get_car_brands_keyboard(language: str = 'uz', brands: list = None) -> InlineKeyboardMarkup:
    """Get car brands keyboard"""
    keyboard = InlineKeyboardBuilder()
    
    if brands:
        for brand in brands:
            brand_name = brand.name_uz if language == 'uz' else brand.name_ru
            keyboard.row(InlineKeyboardButton(
                text=brand_name,
                callback_data=f"brand_{brand.id}"
            ))
    
    if language == 'uz':
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_UZ, callback_data="back_to_search"))
    else:
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_RU, callback_data="back_to_search"))
    
    return keyboard.as_markup()


def get_cities_keyboard(cities: list, language: str = 'uz') -> InlineKeyboardMarkup:
    """Get cities keyboard"""
    keyboard = InlineKeyboardBuilder()
    
    for city in cities:
        city_name = city.name_uz if language == 'uz' else city.name_ru
        keyboard.row(InlineKeyboardButton(
            text=city_name,
            callback_data=f"city_{city.id}"
        ))
    
    if language == 'uz':
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_UZ, callback_data="back_to_brands"))
    else:
        keyboard.row(InlineKeyboardButton(text=Texts.BACK_RU, callback_data="back_to_brands"))
    
    return keyboard.as_markup()


def get_cancel_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get cancel keyboard"""
    if language == 'uz':
        cancel_text = Texts.CANCEL_UZ
    else:
        cancel_text = Texts.CANCEL_RU
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cancel_text)]],
        resize_keyboard=True
    )
    return keyboard


def get_phone_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get phone request keyboard with contact button"""
    if language == 'uz':
        contact_text = "📱 Raqamni yuborish"
        cancel_text = Texts.CANCEL_UZ
    else:
        contact_text = "📱 Отправить номер"
        cancel_text = Texts.CANCEL_RU
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=contact_text, request_contact=True)],
            [KeyboardButton(text=cancel_text)]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_location_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get location request keyboard"""
    if language == 'uz':
        location_text = "📍 Lokatsiyani yuborish"
        cancel_text = Texts.CANCEL_UZ
    else:
        location_text = "📍 Отправить локацию"
        cancel_text = Texts.CANCEL_RU
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=location_text, request_location=True)],
            [KeyboardButton(text=cancel_text)]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_phone_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get phone number keyboard with contact sharing button"""
    if language == 'uz':
        share_text = "📱 Raqamni yuborish"
        cancel_text = Texts.CANCEL_UZ
    else:
        share_text = "📱 Отправить номер"
        cancel_text = Texts.CANCEL_RU
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=share_text, request_contact=True)],
            [KeyboardButton(text=cancel_text)]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_location_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get location keyboard with location sharing button"""
    if language == 'uz':
        share_text = "📍 Lokatsiya yuborish"
        cancel_text = Texts.CANCEL_UZ
    else:
        share_text = "📍 Отправить локацию"
        cancel_text = Texts.CANCEL_RU
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=share_text, request_location=True)],
            [KeyboardButton(text=cancel_text)]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_phone_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get phone request keyboard with contact button"""
    if language == 'uz':
        share_text = "📱 Raqamni yuborish"
        cancel_text = Texts.CANCEL_UZ
    else:
        share_text = "📱 Отправить номер"
        cancel_text = Texts.CANCEL_RU
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=share_text, request_contact=True)],
            [KeyboardButton(text=cancel_text)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_part_categories_keyboard(language: str = 'uz', selected: list = None) -> InlineKeyboardMarkup:
    """Get part categories keyboard with multi-select support"""
    keyboard = InlineKeyboardBuilder()
    
    if selected is None:
        selected = []
    
    for i, category in enumerate(Texts.PART_CATEGORIES):
        text = category[language]
        # Add checkmark if selected
        if i in selected:
            text = f"✅ {text}"
        
        keyboard.row(InlineKeyboardButton(
            text=text,
            callback_data=f"partcat_{i}"
        ))
    
    # Add "Done" button if at least one selected
    if selected:
        if language == 'uz':
            keyboard.row(InlineKeyboardButton(text="✅ Tayyor", callback_data="partcat_done"))
        else:
            keyboard.row(InlineKeyboardButton(text="✅ Готово", callback_data="partcat_done"))
    
    return keyboard.as_markup()
