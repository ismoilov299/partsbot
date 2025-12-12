"""
Admin handlers for shop approval
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.utils import db
from bot.states.user_states import AdminStates

router = Router()


@router.callback_query(F.data.startswith("approve_shop_"))
async def approve_shop_callback(callback: CallbackQuery):
    """Admin approves shop"""
    shop_id = int(callback.data.split("_")[-1])
    
    # Get shop details
    shop = await db.get_shop_by_id(shop_id)
    if not shop:
        await callback.answer("❌ Do'kon topilmadi", show_alert=True)
        return
    
    # Approve shop
    success = await db.approve_shop(shop_id)
    
    if success:
        # Update admin message
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n✅ TASDIQLANDI"
        )
        
        # Notify shop owner
        from aiogram import Bot
        import os
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        
        owner = shop.owner
        notification = f"🎉 Tabriklaymiz!\n\n"
        notification += f"Do'koningiz \"{shop.name}\" tasdiqlandi!\n\n"
        notification += f"Endi foydalanuvchilar sizning do'koningizni topishi mumkin."
        
        try:
            await bot.send_message(
                chat_id=owner.telegram_id,
                text=notification
            )
        except Exception as e:
            print(f"Error notifying owner: {e}")
        
        await callback.answer("✅ Do'kon tasdiqlandi!", show_alert=True)
    else:
        await callback.answer("❌ Tasdiqlashda xatolik", show_alert=True)


@router.callback_query(F.data.startswith("reject_shop_"))
async def reject_shop_callback(callback: CallbackQuery, state: FSMContext):
    """Admin rejects shop - ask for reason"""
    shop_id = int(callback.data.split("_")[-1])
    
    # Get shop details
    shop = await db.get_shop_by_id(shop_id)
    if not shop:
        await callback.answer("❌ Do'kon topilmadi", show_alert=True)
        return
    
    # Save shop_id to state
    await state.update_data(reject_shop_id=shop_id)
    await state.set_state(AdminStates.enter_rejection_reason)
    
    # Ask admin for rejection reason
    await callback.message.answer(
        "❌ Do'konni rad etish sababi:\n\n"
        "Iltimos, rad etish sababini yozing. Bu xabar do'kon egasiga yuboriladi."
    )
    await callback.answer()


@router.message(AdminStates.enter_rejection_reason)
async def process_rejection_reason(message: Message, state: FSMContext):
    """Process rejection reason and notify owner"""
    data = await state.get_data()
    shop_id = data.get('reject_shop_id')
    reason = message.text
    
    # Get shop details
    shop = await db.get_shop_by_id(shop_id)
    if not shop:
        await message.answer("❌ Do'kon topilmadi")
        await state.clear()
        return
    
    owner = shop.owner
    
    # Reject and delete shop
    success = await db.reject_shop(shop_id)
    
    if success:
        # Notify shop owner with reason
        from aiogram import Bot
        import os
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        
        notification = f"❌ Kechirasiz\n\n"
        notification += f"Do'koningiz \"{shop.name}\" tasdiqlanmadi.\n\n"
        notification += f"📝 Sabab:\n{reason}\n\n"
        notification += f"Iltimos, ma'lumotlarni to'g'rilab qaytadan urinib ko'ring."
        
        try:
            await bot.send_message(
                chat_id=owner.telegram_id,
                text=notification
            )
            await message.answer(
                f"✅ Do'kon rad etildi va egasiga sabab yuborildi:\n\n"
                f"📝 {reason}"
            )
        except Exception as e:
            print(f"Error notifying owner: {e}")
            await message.answer(f"❌ Xatolik: {e}")
        
    else:
        await message.answer("❌ Rad etishda xatolik")
    
    await state.clear()
