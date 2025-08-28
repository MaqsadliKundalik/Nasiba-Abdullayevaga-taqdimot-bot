from aiogram.filters import Filter
from database.models.all_models import User
from aiogram.types import Message

class IsNewUser(Filter):
    async def __call__(self, message: Message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        return user is None
    
class IsPremUser(Filter):
    async def __call__(self, message: Message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        return user is not None and user.is_premium