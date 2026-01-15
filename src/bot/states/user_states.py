"""
Bot states for FSM (Finite State Machine)
"""
from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for user registration"""
    choose_language = State()


class ShopSearchStates(StatesGroup):
    """States for shop search"""
    choose_brand = State()
    choose_city = State()
    view_results = State()


class UstaXonaSearchStates(StatesGroup):
    """States for usta xona search"""
    choose_service_types = State()
    choose_brand = State()
    choose_city = State()
    view_results = State()


class ShopAddStates(StatesGroup):
    """States for adding a shop"""
    enter_shop_name = State()
    enter_phone = State()
    choose_city = State()
    share_location = State()
    enter_address = State()
    upload_photo = State()
    choose_brands = State()
    choose_part_categories = State()
    enter_description = State()
    confirm = State()


class UstaXonaAddStates(StatesGroup):
    """States for adding a service center (usta xona)"""
    enter_service_name = State()
    enter_phone = State()
    choose_city = State()
    share_location = State()
    enter_address = State()
    upload_photo = State()
    choose_brands = State()
    choose_service_types = State()
    enter_description = State()
    confirm = State()


class RequestStates(StatesGroup):
    """States for leaving a request"""
    enter_description = State()
    enter_phone = State()
    choose_city = State()
    confirm = State()


class AdminStates(StatesGroup):
    """States for admin actions"""
    enter_rejection_reason = State()
