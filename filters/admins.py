from aiogram.filters import Filter
from config import ADMIN
from aiogram.types import Message

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == int(ADMIN)