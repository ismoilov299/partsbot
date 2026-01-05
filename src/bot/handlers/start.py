"""
Start command handler and language selection
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_language_keyboard, get_main_menu_keyboard, Texts
from bot.utils import db
from bot.states import RegistrationStates

router = Router()


@router.message(Command("cancel"),state="*")
async def cmd_cancel(message: Message, state: FSMContext):
    """Handle /cancel command - clear state and return to main menu"""
    current_state = await state.get_state()
    
    if current_state is None:
        # No active state
        user = await db.get_user(message.from_user.id)
        if user:
            if user.language == 'uz':
                await message.answer("Hech qanday faol jarayon yo'q.")
            else:
                await message.answer("Нет активного процесса.")
        return
    
    # Clear the state
    await state.clear()
    
    user = await db.get_user(message.from_user.id)
    if user:
        if user.language == 'uz':
            text = f"❌ Bekor qilindi.\n\n{Texts.MAIN_MENU_UZ}:"
        else:
            text = f"❌ Отменено.\n\n{Texts.MAIN_MENU_RU}:"
        
        await message.answer(
            text,
            reply_markup=get_main_menu_keyboard(user.language)
        )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    user = await db.get_user(message.from_user.id)
    
    if user is None:
        # New user - ask for language
        await message.answer(
            f"{Texts.CHOOSE_LANGUAGE_UZ}\n\n{Texts.CHOOSE_LANGUAGE_RU}",
            reply_markup=get_language_keyboard()
        )
        await state.set_state(RegistrationStates.choose_language)
    else:
        # Existing user - show main menu
        if user.language == 'uz':
            welcome_text = f"Assalomu alaykum, {user.first_name}! 👋\n\n{Texts.MAIN_MENU_UZ}:"
        else:
            welcome_text = f"Здравствуйте, {user.first_name}! 👋\n\n{Texts.MAIN_MENU_RU}:"
        
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard(user.language)
        )


@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    """Process language selection"""
    language = callback.data.split("_")[1]
    
    # Create or update user
    user = await db.get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name
    )
    await db.update_user_language(callback.from_user.id, language)
    
    # Show welcome message and main menu
    if language == 'uz':
        welcome_text = f"Xush kelibsiz, {callback.from_user.first_name}! 👋\n\n{Texts.MAIN_MENU_UZ}:"
    else:
        welcome_text = f"Добро пожаловать, {callback.from_user.first_name}! 👋\n\n{Texts.MAIN_MENU_RU}:"
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(language)
    )
    
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Return to main menu"""
    user = await db.get_user(callback.from_user.id)
    
    if user:
        if user.language == 'uz':
            text = f"{Texts.MAIN_MENU_UZ}:"
        else:
            text = f"{Texts.MAIN_MENU_RU}:"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_main_menu_keyboard(user.language)
        )
    
    await state.clear()
    await callback.answer()


@router.message()
async def handle_unknown_message(message: Message, state: FSMContext):
    """Handle all unhandled messages - show main menu"""
    user = await db.get_user(message.from_user.id)
    
    if user is None:
        # New user - ask for language
        await message.answer(
            f"{Texts.CHOOSE_LANGUAGE_UZ}\n\n{Texts.CHOOSE_LANGUAGE_RU}",
            reply_markup=get_language_keyboard()
        )
        await state.set_state(RegistrationStates.choose_language)
    else:
        # Show main menu
        if user.language == 'uz':
            text = f"{Texts.MAIN_MENU_UZ}:"
        else:
            text = f"{Texts.MAIN_MENU_RU}:"
        
        await message.answer(
            text,
            reply_markup=get_main_menu_keyboard(user.language)
        )
        await state.clear()
