from aiogram.filters import Filter
from database.models.all_models import User, UserQuarterSubscription, QuarterSettings
from aiogram.types import Message

class IsNewUser(Filter):
    async def __call__(self, message: Message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        return user is None
    
class IsPremUser(Filter):
    async def __call__(self, message: Message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        return user is not None and user.is_premium

class HasQuarterAccess(Filter):
    def __init__(self, quarter_number: int = None):
        self.quarter_number = quarter_number

    async def __call__(self, message: Message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        if not user:
            return False
        
        # Agar to'liq premium bo'lsa
        if user.is_premium:
            return True
        
        # Agar quarter_number berilmagan bo'lsa, hozirgi chorakni tekshir
        if self.quarter_number is None:
            quarter_settings = await QuarterSettings.first()
            if not quarter_settings:
                return False
            check_quarter = quarter_settings.current_quarter
        else:
            check_quarter = self.quarter_number
        
        # Specific chorak uchun ruxsat bor yoki yo'qligini tekshir
        subscription = await UserQuarterSubscription.get_or_none(
            user=user, 
            quarter_number=check_quarter, 
            is_active=True
        )
        return subscription is not None