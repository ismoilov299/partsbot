"""
Admin handlers for shop approval
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.utils import db

router = Router()


@router.callback_query(F.data.startswith("approve_shop_"))
async def approve_shop_callback(callback: CallbackQuery):
    """Admin approves shop"""
    shop_id = int(callback.data.split("_")[-1])
    
    # Get shop details
    shop = await db.get_shop_by_id(shop_id)
    if not shop:
        await callback.answer("❌ Магазин не найден", show_alert=True)
        return
    
    # Approve shop
    success = await db.approve_shop(shop_id)
    
    if success:
        # Update admin message
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n✅ ОДОБРЕНО"
        )
        
        # Notify shop owner
        from aiogram import Bot
        import os
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        
        owner = shop.owner
        if owner.language == 'uz':
            notification = f"🎉 Tabriklaymiz!\n\n"
            notification += f"Do'koningiz \"{shop.name}\" tasdiqlandi!\n\n"
            notification += f"Endi foydalanuvchilar sizning do'koningizni topishi mumkin."
        else:
            notification = f"🎉 Поздравляем!\n\n"
            notification += f"Ваш магазин \"{shop.name}\" одобрен!\n\n"
            notification += f"Теперь пользователи могут найти ваш магазин."
        
        try:
            await bot.send_message(
                chat_id=owner.telegram_id,
                text=notification
            )
        except Exception as e:
            print(f"Error notifying owner: {e}")
        
        await callback.answer("✅ Магазин одобрен!", show_alert=True)
    else:
        await callback.answer("❌ Ошибка при одобрении", show_alert=True)


@router.callback_query(F.data.startswith("reject_shop_"))
async def reject_shop_callback(callback: CallbackQuery):
    """Admin rejects shop"""
    shop_id = int(callback.data.split("_")[-1])
    
    # Get shop details
    shop = await db.get_shop_by_id(shop_id)
    if not shop:
        await callback.answer("❌ Магазин не найден", show_alert=True)
        return
    
    owner = shop.owner
    
    # Reject and delete shop
    success = await db.reject_shop(shop_id)
    
    if success:
        # Update admin message
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n❌ ОТКЛОНЕНО"
        )
        
        # Notify shop owner
        from aiogram import Bot
        import os
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        
        if owner.language == 'uz':
            notification = f"❌ Kechirasiz\n\n"
            notification += f"Do'koningiz \"{shop.name}\" tasdiqlanmadi.\n\n"
            notification += f"Iltimos, ma'lumotlarni tekshirib qaytadan urinib ko'ring."
        else:
            notification = f"❌ К сожалению\n\n"
            notification += f"Ваш магазин \"{shop.name}\" не был одобрен.\n\n"
            notification += f"Пожалуйста, проверьте данные и попробуйте снова."
        
        try:
            await bot.send_message(
                chat_id=owner.telegram_id,
                text=notification
            )
        except Exception as e:
            print(f"Error notifying owner: {e}")
        
        await callback.answer("❌ Магазин отклонен и удален", show_alert=True)
    else:
        await callback.answer("❌ Ошибка при отклонении", show_alert=True)
